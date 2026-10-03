#!/usr/bin/env bash
# Builds Step Planner as an Android app (APK) without the Android SDK or Gradle.
# Tools come from Maven Central (aapt2 + framework resources from Apktool, dx, apksig) and npm (three.js).
# Usage: ./build-apk.sh [versionName]      Output: dist/StepPlanner-<version>.apk
set -euo pipefail
cd "$(dirname "$0")"
HERE=$PWD WEB=$PWD/..
VERSION=${1:-$(date +%Y.%m.%d)}
CODE=$(( $(date +%s) / 60 ))
TOOLS=${TOOLS_DIR:-$HERE/.tools}
OUT=$HERE/build
mkdir -p "$TOOLS" "$OUT" "$HERE/dist"
M=https://repo1.maven.org/maven2
fetch() { [ -s "$TOOLS/$2" ] || curl -fsSL -o "$TOOLS/$2" "$1"; }

# --- tools ---
fetch "$M/org/apktool/apktool-lib/3.0.3/apktool-lib-3.0.3.jar" apktool-lib.jar
fetch "$M/org/robolectric/android-all/14-robolectric-10818077/android-all-14-robolectric-10818077.jar" android-all.jar
fetch "$M/com/jakewharton/android/repackaged/dalvik-dx/16.0.1/dalvik-dx-16.0.1.jar" dx.jar
fetch "$M/com/android/tools/build/apksig/2.3.0/apksig-2.3.0.jar" apksig.jar
if [ ! -x "$TOOLS/aapt2" ]; then
  unzip -o -q -j "$TOOLS/apktool-lib.jar" prebuilt/linux/aapt2 prebuilt/android-framework.jar -d "$TOOLS"
  chmod +x "$TOOLS/aapt2"
fi
if [ ! -s "$TOOLS/three.min.js" ]; then
  (cd "$TOOLS" && npm pack three@0.147.0 --silent >/dev/null && tar -xzf three-0.147.0.tgz \
    package/build/three.min.js package/examples/js/controls/OrbitControls.js && mv package/build/three.min.js package/examples/js/controls/OrbitControls.js . && rm -rf package three-0.147.0.tgz)
fi

# --- web app, with three.js bundled so 3D works offline ---
rm -rf "$OUT"; mkdir -p "$OUT/assets/www/vendor" "$OUT/classes" "$OUT/res"
cp "$TOOLS/three.min.js" "$TOOLS/OrbitControls.js" "$OUT/assets/www/vendor/"
cp "$WEB/icon.svg" "$WEB/icon-192.png" "$OUT/assets/www/"
sed -e 's#https://cdn.jsdelivr.net/npm/three@0.147.0/build/three.min.js#vendor/three.min.js#' \
    -e 's#https://cdn.jsdelivr.net/npm/three@0.147.0/examples/js/controls/OrbitControls.js#vendor/OrbitControls.js#' \
    -e '/rel="manifest"/d' "$WEB/index.html" > "$OUT/assets/www/index.html"
grep -q 'vendor/three.min.js' "$OUT/assets/www/index.html" || { echo "three.js path not rewritten"; exit 1; }

# --- launcher icons (legacy + adaptive foreground) ---
cp -r "$HERE/res/." "$OUT/res/"
for d in mdpi:48:108 hdpi:72:162 xhdpi:96:216 xxhdpi:144:324 xxxhdpi:192:432; do
  IFS=: read -r name px fg <<< "$d"
  mkdir -p "$OUT/res/mipmap-$name"
  convert "$WEB/icon-512.png" -resize "${px}x${px}" "$OUT/res/mipmap-$name/ic_launcher.png"
  # foreground: the artwork at 72% inside the 108dp adaptive canvas, on transparent
  inner=$(( fg * 72 / 100 ))
  convert "$WEB/icon-512.png" -resize "${inner}x${inner}" -background none -gravity center -extent "${fg}x${fg}" "$OUT/res/mipmap-$name/ic_launcher_foreground.png"
done

# --- code: javac -> dx ---
javac -nowarn --release 8 -cp "$TOOLS/android-all.jar" -d "$OUT/classes" $(find "$HERE/src" -name '*.java') 2>&1 | grep -v "^warning\|^Note\|^[0-9] warning" || true
java -cp "$TOOLS/dx.jar" com.android.dx.command.Main --dex --min-sdk-version=26 --output="$OUT/classes.dex" "$OUT/classes"

# --- resources + manifest: aapt2 ---
"$TOOLS/aapt2" compile --dir "$OUT/res" -o "$OUT/res.zip"
"$TOOLS/aapt2" link -o "$OUT/unsigned.apk" -I "$TOOLS/android-framework.jar" --manifest "$HERE/AndroidManifest.xml" \
  --min-sdk-version 29 --target-sdk-version 34 --version-code "$CODE" --version-name "$VERSION" \
  -A "$OUT/assets" --auto-add-overlay "$OUT/res.zip"
(cd "$OUT" && zip -q -j unsigned.apk classes.dex)

# --- align + sign ---
python3 "$HERE/zipalign.py" "$OUT/unsigned.apk" "$OUT/aligned.apk"
KEY=$HERE/release.p12 PASS=${KEY_PASS:-stepplanner}
[ -s "$KEY" ] || keytool -genkeypair -keystore "$KEY" -storetype PKCS12 -storepass "$PASS" -keypass "$PASS" -alias stepplanner \
  -keyalg RSA -keysize 3072 -validity 18250 -dname "CN=Block Step Planner, O=Cygnus Eco" 2>/dev/null
javac -nowarn -cp "$TOOLS/apksig.jar" -d "$OUT" "$HERE/SignApk.java"
APK="$HERE/dist/StepPlanner-$VERSION.apk"
java --add-exports java.base/sun.security.x509=ALL-UNNAMED --add-exports java.base/sun.security.pkcs=ALL-UNNAMED --add-exports java.base/sun.security.util=ALL-UNNAMED -cp "$TOOLS/apksig.jar:$OUT" SignApk "$OUT/aligned.apk" "$APK" "$KEY" "$PASS" stepplanner
python3 "$HERE/zipalign.py" --check "$APK"
echo "Built $APK ($(du -h "$APK" | cut -f1))"
