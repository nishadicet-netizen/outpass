package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

public class GuardSendLateComing extends AppCompatActivity implements JsonResponse, AdapterView.OnItemSelectedListener {
    String[] name,student_id,val;
    Spinner s1;
    Button b1;
    EditText e1;
    String late;
    public static String student_ids;
    ListView lv1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_guard_send_late_coming);
        s1=(Spinner) findViewById(R.id.sppet);
        s1.setOnItemSelectedListener(this);

        e1=(EditText)findViewById(R.id.etdetails) ;


        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) GuardSendLateComing.this;
        String q = "/students";
        q=q.replace(" ","%20");
        JR.execute(q);





        b1=(Button)findViewById(R.id.btpet);
        b1.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub
                late=e1.getText().toString();

                if(late.equalsIgnoreCase(""))
                {
                    e1.setError("No value for Late By");
                    e1.setFocusable(true);
                }

                else{
                    JsonReq JR=new JsonReq();
                    JR.json_response=(JsonResponse) GuardSendLateComing.this;
                    String q = "/guard_send_late?student_id="+student_ids+"&late="+late;
                    q=q.replace(" ","%20");
                    JR.execute(q);
                }
            }
        });
    }


    public void response(JSONObject jo) {
        // TODO Auto-generated method stub

        try {
            String method = jo.getString("method");
            Toast.makeText(getApplicationContext(), method, Toast.LENGTH_LONG).show();

            if (method.equalsIgnoreCase("guard_send_late")) {
                String status = jo.getString("status");
                Log.d("pearl",status);
                if (status.equalsIgnoreCase("success")) {

                    Toast.makeText(getApplicationContext(), "  Success", Toast.LENGTH_LONG).show();

                    startActivity(new Intent(getApplicationContext(), GuardSendLateComing.class));
                } else {
                    Toast.makeText(getApplicationContext(), " failed", Toast.LENGTH_LONG).show();
                }
            }


           else if (method.equalsIgnoreCase("students")) {
                String status = jo.getString("status");
                Log.d("pearl", status);

                if (status.equalsIgnoreCase("success")) {
                    JSONArray ja1 = (JSONArray) jo.getJSONArray("data");

                    student_id=new String[ja1.length()];
                    name = new String[ja1.length()];
                    val = new String[ja1.length()];

                    for (int i = 0; i < ja1.length(); i++) {
                        student_id[i]=ja1.getJSONObject(i).getString("student_id");
                        name[i] = ja1.getJSONObject(i).getString("name");

                        val[i] = "name  :  " + name[i];


                    }
                    ArrayAdapter<String> ar = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_list_item_1, val);
                    s1.setAdapter(ar);
                    //startActivity(new Intent(getApplicationContext(),User_Post_Disease.class));
                } else {
                    Toast.makeText(getApplicationContext(), "No data!!", Toast.LENGTH_LONG).show();

                }
            }
        }
        catch (Exception e){
            // TODO: handle exception
        }

    }



    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

        student_ids=student_id[position];

    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }
}