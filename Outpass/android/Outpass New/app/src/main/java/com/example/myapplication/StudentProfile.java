package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

public class StudentProfile extends AppCompatActivity implements JsonResponse {
    ListView lv1;


    String[] first_name,last_name,phone,email,course,batch,val;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_profile);


        lv1=(ListView)findViewById(R.id.lv1);


        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) StudentProfile.this;
        String q = "/view_profile?login_id="+Login.logid;
        q=q.replace(" ","%20");
        JR.execute(q);
    }




    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method=jo.getString("method");
            if(method.equalsIgnoreCase("view_profile")){
                String status=jo.getString("status");
                Log.d("pearl",status);
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_SHORT).show();
                if(status.equalsIgnoreCase("success")){

                    JSONArray ja1=(JSONArray)jo.getJSONArray("data");

                    first_name=new String[ja1.length()];
                    last_name=new String[ja1.length()];
                    phone=new String[ja1.length()];
                    email=new String[ja1.length()];

                    course=new String[ja1.length()];
                    batch=new String[ja1.length()];
//                    product_name=new String[ja1.length()];




                    val=new String[ja1.length()];



                    for(int i = 0;i<ja1.length();i++)
                    {


                        first_name[i]=ja1.getJSONObject(i).getString("first_name");
                        last_name[i]=ja1.getJSONObject(i).getString("last_name");
                        phone[i]=ja1.getJSONObject(i).getString("phone");
                        email[i]=ja1.getJSONObject(i).getString("email");


                        course[i]=ja1.getJSONObject(i).getString("course_name");
                        batch[i]=ja1.getJSONObject(i).getString("end_year");
//                        place[i]=ja1.getJSONObject(i).getString("place");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i]="FirstName: "+first_name[i]+"\nLastName:  "+last_name[i]+"\nPhone:  "+phone[i]+"\nEmail:  "+email[i]+"\nCourse:  "+course[i]+"\nBatch:  "+batch[i];


                    }
                    ArrayAdapter<String> ar=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,val);
                    lv1.setAdapter(ar);



                }

                else {
                    Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();

                }
            }


            if(method.equalsIgnoreCase("teacher_send_outpass_request"))
            {
                String status=jo.getString("status");
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
                if(status.equalsIgnoreCase("success"))
                {
                    Toast.makeText(getApplicationContext()," Submitted!", Toast.LENGTH_LONG).show();
                    startActivity(new Intent(getApplicationContext(), TeacherRequestOutpass.class));
                }
                else{
                    Toast.makeText(getApplicationContext(),"Failed", Toast.LENGTH_LONG).show();
                }
            }
        }catch (Exception e)
        {
            // TODO: handle exception

            Toast.makeText(getApplicationContext(),e.toString(), Toast.LENGTH_LONG).show();
        }



    }
}