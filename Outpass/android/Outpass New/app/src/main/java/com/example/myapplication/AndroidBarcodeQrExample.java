package com.example.myapplication;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.util.Locale;

public class AndroidBarcodeQrExample extends AppCompatActivity implements JsonResponse
{


	public static String pass_id;
	/** Called when the activity is first created. */
	String method="getslotidandlocid";
	String soapaction="http://tempuri.org/getslotidandlocid";
	static final String ACTION_SCAN = "com.google.zxing.client.android.SCAN";
	  public static TextToSpeech t1;
	@Override
	public void onCreate(Bundle savedInstanceState) 
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		 
		 t1=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() 
		 {
	         @Override
	         public void onInit(int status) 
	         {
	        	 
	            if(status != TextToSpeech.ERROR) 
	            {
	               t1.setLanguage(Locale.UK);
	               //t1.speak("hello", params)
	              // t1.speak("success", TextToSpeech.QUEUE_FLUSH, null);
					
	            }
	            
	            else
	            {
	            	//t1.speak("found some error", TextToSpeech.QUEUE_FLUSH, null);
					
	            }
	         }
	      });

	}

	public void scanBar(View v) {
		try {
			Intent intent = new Intent(ACTION_SCAN);
			intent.putExtra("SCAN_MODE", "PRODUCT_MODE");
			startActivityForResult(intent, 0);
		} catch (ActivityNotFoundException anfe) {
			showDialog(AndroidBarcodeQrExample.this, "No Scanner Found", "Download a scanner code activity?", "Yes", "No").show();
		}
	}

	public void scanQR(View v) {
		try {
			Intent intent = new Intent(ACTION_SCAN);
			intent.putExtra("SCAN_MODE", "QR_CODE_MODE");
			startActivityForResult(intent, 0);
		} catch (ActivityNotFoundException anfe) {
			showDialog(AndroidBarcodeQrExample.this, "No Scanner Found", "Download a scanner code activity?", "Yes", "No").show();
		}
	}

	private static AlertDialog showDialog(final Activity act, CharSequence title, CharSequence message, CharSequence buttonYes, CharSequence buttonNo) {
		AlertDialog.Builder downloadDialog = new AlertDialog.Builder(act);
		downloadDialog.setTitle(title);
		downloadDialog.setMessage(message);
		downloadDialog.setPositiveButton(buttonYes, new DialogInterface.OnClickListener() {
			public void onClick(DialogInterface dialogInterface, int i) {
				Uri uri = Uri.parse("market://search?q=pname:" + "com.google.zxing.client.android");
				Intent intent = new Intent(Intent.ACTION_VIEW, uri);
				try {
					act.startActivity(intent);
				} catch (ActivityNotFoundException anfe) {

				}
			}
		});
		downloadDialog.setNegativeButton(buttonNo, new DialogInterface.OnClickListener() {
			public void onClick(DialogInterface dialogInterface, int i) 
			{
			}
		});
		return downloadDialog.show();
	}

//	 public void onPause(){
//	      if(t1 !=null){
//	         t1.stop();
//	         t1.shutdown();
//	      }
//	      super.onPause();
//	   }
	public void onActivityResult(int requestCode, int resultCode, Intent intent) {
		if (requestCode == 0) {
			if (resultCode == RESULT_OK) {
				String contents = intent.getStringExtra("SCAN_RESULT");
				String format = intent.getStringExtra("SCAN_RESULT_FORMAT");

				Toast toast = Toast.makeText(this, "Content:" + contents + " Format:" + format, Toast.LENGTH_LONG);
				toast.show();
				

				if(contents.equalsIgnoreCase(""))
				{

					Toast toast1 = Toast.makeText(this, "The Scanned Code is not Correct", Toast.LENGTH_LONG);
					toast.show();
				}
				else{
					pass_id=contents;

					startActivity(new Intent(getApplicationContext(), GuardViewDeatils.class));

				}
				
				
				
//				try{
//					SharedPreferences sh=PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
//					SoapObject sop=new SoapObject(MainActivity.namespace,method);
//					sop.addProperty("qrid",contents);
//						
//					SoapSerializationEnvelope ssc=new SoapSerializationEnvelope(SoapEnvelope.VER11);
//					ssc.setOutputSoapObject(sop);
//					ssc.dotNet=true;
//					HttpTransportSE http=new HttpTransportSE(MainActivity.url);
//					http.call(soapaction, ssc);
//					String result=ssc.getResponse().toString();
//					Toast.makeText(getApplicationContext(), result, Toast.LENGTH_SHORT).show();
//					
//					if(result.equalsIgnoreCase("no"))
//					{
//						Toast.makeText(getApplicationContext(), "invalid code", Toast.LENGTH_SHORT).show();
//						
//						
//					}
//					else
//					{
//						
//						String [] bc= result.split("\\#");
//						SharedPreferences sh1=PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
//						Editor ed=sh1.edit();
//						ed.putString("lid", bc[0]);
//						ed.putString("sid", bc[1]);
//						ed.commit();
//						
//						//Intent aa=new Intent(getApplicationContext(), alrt.class);
//					   // startService(aa);
//					    Intent af=new Intent(getApplicationContext(), StatusUpdate.class);
//					    startActivity(af);
//						
//						
//						//Toast.makeText(getApplicationContext(),"getslotidandlocid...."+ result, Toast.LENGTH_SHORT).show();
//						
//					}
//					
//					
//				}
//				catch(Exception ex)
//				{
//					Toast.makeText(getApplicationContext(), "error in alrt", Toast.LENGTH_SHORT).show();
//					
//				}
//					
//					
		
				
				
				
			}
		}
	}
	
	@Override
	public void response(JSONObject jo) {
		// TODO Auto-generated method stub
		
		

		try {
			
			String method=jo.getString("method");
			
		 if(method.equalsIgnoreCase("view_qr_code"))
			{
				String status=jo.getString("status");
				Toast.makeText(getApplicationContext(), status, Toast.LENGTH_LONG).show();
				if(status.equalsIgnoreCase("success"))
				{
					Toast.makeText(getApplicationContext(), "Scan Successful.\nYour Order is Picked UP.", Toast.LENGTH_LONG).show();
					startActivity(new Intent(getApplicationContext(),Homepage.class));
				}

				else 
				{
					Toast.makeText(getApplicationContext(), "Not Successfull!!!! \n Try Again......", Toast.LENGTH_LONG).show();
				}
			}
			
	}catch (Exception e) {
	// TODO: handle exception
	
	  Toast.makeText(getApplicationContext(),e.toString(), Toast.LENGTH_LONG).show();
	}

	}
		

	
	
}