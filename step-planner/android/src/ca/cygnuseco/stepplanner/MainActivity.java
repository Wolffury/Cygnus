package ca.cygnuseco.stepplanner;

import android.app.Activity;
import android.content.ClipData;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.OutputStream;

/**
 * Block Step Planner runs as a web page bundled in the app (assets/www). This activity hosts it in a
 * WebView, opens the system file picker for photo and file inputs, and gives the page a small bridge
 * (window.AndroidBridge) to save exported files into Downloads/Block Step Planner.
 */
public class MainActivity extends Activity {
    private static final int PICK_FILES = 41;
    private WebView web;
    private ValueCallback<Uri[]> pendingPick;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setTextZoom(100);

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (pendingPick != null) pendingPick.onReceiveValue(null);
                pendingPick = callback;
                Intent pick = params.createIntent();
                if (params.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE) pick.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                try {
                    startActivityForResult(pick, PICK_FILES);
                } catch (Exception e) {
                    pendingPick = null;
                    return false;
                }
                return true;
            }
        });
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                if ("file".equals(u.getScheme())) return false;
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, u)); // links open in the browser
                } catch (Exception ignored) {
                }
                return true;
            }
        });
        web.addJavascriptInterface(new Bridge(), "AndroidBridge");
        setContentView(web);
        if (state != null) web.restoreState(state);
        else web.loadUrl("file:///android_asset/www/index.html");
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != PICK_FILES || pendingPick == null) return;
        Uri[] result = null;
        if (resultCode == RESULT_OK && data != null) {
            ClipData clip = data.getClipData();
            if (clip != null && clip.getItemCount() > 0) {
                result = new Uri[clip.getItemCount()];
                for (int i = 0; i < clip.getItemCount(); i++) result[i] = clip.getItemAt(i).getUri();
            } else if (data.getData() != null) {
                result = new Uri[] { data.getData() };
            }
        }
        pendingPick.onReceiveValue(result);
        pendingPick = null;
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) web.goBack();
        else super.onBackPressed();
    }

    /** Methods the page can call as window.AndroidBridge.* */
    public class Bridge {
        /** Saves base64 data to Downloads/Block Step Planner. Returns the content URI, or "" on failure. */
        @JavascriptInterface
        public String saveFile(String name, String base64, String mime) {
            try {
                byte[] bytes = Base64.decode(base64, Base64.DEFAULT);
                ContentValues cv = new ContentValues();
                cv.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
                cv.put(MediaStore.MediaColumns.MIME_TYPE, mime == null || mime.isEmpty() ? "application/octet-stream" : mime);
                cv.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/Block Step Planner");
                ContentResolver cr = getContentResolver();
                Uri uri = cr.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, cv);
                if (uri == null) return "";
                OutputStream os = cr.openOutputStream(uri);
                if (os == null) return "";
                os.write(bytes);
                os.close();
                return uri.toString();
            } catch (Exception e) {
                return "";
            }
        }

        /** Opens the Android share sheet for a file saved with saveFile (email, Drive, messages…). */
        @JavascriptInterface
        public void shareFile(final String uri, final String mime) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    try {
                        Intent send = new Intent(Intent.ACTION_SEND);
                        send.setType(mime == null || mime.isEmpty() ? "application/octet-stream" : mime);
                        send.putExtra(Intent.EXTRA_STREAM, Uri.parse(uri));
                        send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                        startActivity(Intent.createChooser(send, "Send file"));
                    } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "Couldn't open sharing.", Toast.LENGTH_SHORT).show();
                    }
                }
            });
        }

        @JavascriptInterface
        public boolean isApp() {
            return true;
        }
    }
}
