package com.example.myapplication;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

public class Login extends AppCompatActivity implements JsonResponse
{

	EditText e1,e2;
	Button b1;
	String url;
	TextView t2,t3;
	SharedPreferences sh;
	String username,password;
	public static String logid;
	
    @TargetApi(Build.VERSION_CODES.GINGERBREAD) @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        sh=PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        try 
		{	
			if(Build.VERSION.SDK_INT>9)
			{
				StrictMode.ThreadPolicy policy=new StrictMode.ThreadPolicy.Builder().permitAll().build();
				StrictMode.setThreadPolicy(policy);
			}			
		} 
		catch (Exception e) 
		{
			// TODO: handle exception
		}
        e1=(EditText) findViewById(R.id.editText1);
        e2=(EditText) findViewById(R.id.editText2);
        
//        t2=(TextView) findViewById(R.id.textView2);
//		t3=(TextView) findViewById(R.id.textView3);

//        startService(new Intent(getApplicationContext(),LocationService.class));
        
//        t2.setOnClickListener(new View.OnClickListener()
//        {
//
//			@Override
//			public void onClick(View arg0)
//			{
//				// TODO Auto-generated method stub
//				Intent b=new Intent(getApplicationContext(),Register.class);
//				startActivity(b);
//			}
//		});
//		t3.setOnClickListener(new View.OnClickListener()
//		{
//
//			@Override
//			public void onClick(View arg0)
//			{
//				// TODO Auto-generated method stub
//				Intent b=new Intent(getApplicationContext(),DonorRegister.class);
//				startActivity(b);
//			}
//		});


        b1=(Button) findViewById(R.id.button1);
        b1.setOnClickListener(new View.OnClickListener() 
        {
			
			@Override
			public void onClick(View arg0) 
			{
				username=e1.getText().toString();
				password=e2.getText().toString();
				if(username.equalsIgnoreCase(""))
				{
					e1.setError("Enter username");
					e1.setFocusable(true);
				}			
				else if(password.equalsIgnoreCase(""))
				{
					e2.setError("Enter Password");
					e2.setFocusable(true);
				}
				else
				{
				
					JsonReq JR= new JsonReq();
					JR.json_response=(JsonResponse) Login.this;
					String q="/login?username=" + username + "&password=" + password;
					JR.execute(q);
					
				}
			}

			
		});
    }
    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {
            String status = jo.getString("status");
            Log.d("result", status);
            if (status.equalsIgnoreCase("success")) {
                JSONArray ja = (JSONArray) jo.getJSONArray("data");
                logid = ja.getJSONObject(0).getString("login_id");
                String type = ja.getJSONObject(0).getString("usertype");
                Editor ed = sh.edit();
                ed.putString("logid", logid);
                ed.commit();

                if (type.equals("teacher"))
                {
                    startActivity(new Intent(getApplicationContext(),Homepage.class));
                 
                }
                else if(type.equals("student"))
				{
					startActivity(new Intent(getApplicationContext(), StudentHome.class));
				}
				else if(type.equals("guard"))
				{
					startActivity(new Intent(getApplicationContext(), GuardHome.class));
				}
                else
                    Toast.makeText(getApplicationContext(), "Login failed..!!", Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), "Login failed.TRY AGAIN!!", Toast.LENGTH_LONG).show();
            }
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
        }
    }


    
    public void onBackPressed() 
	{
		// TODO Auto-generated method stub
		super.onBackPressed();
		Intent b=new Intent(getApplicationContext(), IPSettings.class);
		startActivity(b);
	}

}
