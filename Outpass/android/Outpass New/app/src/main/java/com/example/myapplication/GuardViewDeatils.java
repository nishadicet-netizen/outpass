package com.example.myapplication;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

public class GuardViewDeatils extends AppCompatActivity implements JsonResponse {


    ListView lv1;

    String request,date,reason,duration;
    String[] dates,reasons,time,durations,pass_id,val,statuss,course_name,first_name,last_name,place,email;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_guard_view_deatils);

        lv1=(ListView)findViewById(R.id.lv1);

        JsonReq jr= new JsonReq();
        jr.json_response=(JsonResponse) GuardViewDeatils.this;
        String q="/view_qr_code?outpass_id="+AndroidBarcodeQrExample.pass_id;
        q.replace("", "%20");
        jr.execute(q);

    }


    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method=jo.getString("method");
            if(method.equalsIgnoreCase("view_qr_code")){
                String status=jo.getString("status");
                Log.d("pearl",status);
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_SHORT).show();
                if(status.equalsIgnoreCase("success")){

                    JSONArray ja1=(JSONArray)jo.getJSONArray("data");

                    pass_id=new String[ja1.length()];
                    dates=new String[ja1.length()];
                    reasons=new String[ja1.length()];
                    time=new String[ja1.length()];

                    statuss=new String[ja1.length()];
                    first_name=new String[ja1.length()];
                    last_name=new String[ja1.length()];
                    course_name=new String[ja1.length()];




                    val=new String[ja1.length()];



                    for(int i = 0;i<ja1.length();i++)
                    {


                        pass_id[i]=ja1.getJSONObject(i).getString("pass_id");
                        dates[i]=ja1.getJSONObject(i).getString("request_date");
                        reasons[i]=ja1.getJSONObject(i).getString("reason");
                        time[i]=ja1.getJSONObject(i).getString("request_time");


                        statuss[i]=ja1.getJSONObject(i).getString("status");
                        first_name[i]=ja1.getJSONObject(i).getString("first_name");
                        last_name[i]=ja1.getJSONObject(i).getString("last_name");
                        course_name[i]=ja1.getJSONObject(i).getString("course_name");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i]="FirstName: "+first_name[i]+"\nLastName: "+last_name[i]+"\nCourse: "+course_name[i]+"\nReason: "+reasons[i]+"\nDate:  "+dates[i]+"\nTime:  "+time[i]+"\nStatus:  "+statuss[i];


                    }
                    ArrayAdapter<String> ar=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,val);
                    lv1.setAdapter(ar);



                }

                else {
                    Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();

                }
            }


            if(method.equalsIgnoreCase("view_qr_code_for_teacher")){
                String status=jo.getString("status");
                Log.d("pearl",status);
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_SHORT).show();
                if(status.equalsIgnoreCase("success")){

                    JSONArray ja1=(JSONArray)jo.getJSONArray("data");

                    pass_id=new String[ja1.length()];
                    dates=new String[ja1.length()];
                    reasons=new String[ja1.length()];
                    time=new String[ja1.length()];

                    statuss=new String[ja1.length()];
                    first_name=new String[ja1.length()];
                    last_name=new String[ja1.length()];
                    place=new String[ja1.length()];
                    email=new String[ja1.length()];




                    val=new String[ja1.length()];



                    for(int i = 0;i<ja1.length();i++)
                    {


                        pass_id[i]=ja1.getJSONObject(i).getString("pass_id");
                        dates[i]=ja1.getJSONObject(i).getString("request_date");
                        reasons[i]=ja1.getJSONObject(i).getString("reason");
                        time[i]=ja1.getJSONObject(i).getString("request_time");


                        statuss[i]=ja1.getJSONObject(i).getString("status");
                        first_name[i]=ja1.getJSONObject(i).getString("first_name");
                        last_name[i]=ja1.getJSONObject(i).getString("last_name");
                        place[i]=ja1.getJSONObject(i).getString("place");
                        email[i]=ja1.getJSONObject(i).getString("email");


                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i]="FirstName: "+first_name[i]+"\nLastName: "+last_name[i]+"\nPlace: "+place[i]+"\nEmail: "+email[i]+"\nReason: "+reasons[i]+"\nDate:  "+dates[i]+"\nTime:  "+time[i]+"\nStatus:  "+statuss[i];


                    }
                    ArrayAdapter<String> ar=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,val);
                    lv1.setAdapter(ar);



                }

                else {
                    Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();

                }
            }


//            if(method.equalsIgnoreCase("teacher_send_leave_request"))
//            {
//                String status=jo.getString("status");
//                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
//                if(status.equalsIgnoreCase("success"))
//                {
//                    Toast.makeText(getApplicationContext()," Submitted!", Toast.LENGTH_LONG).show();
//                    startActivity(new Intent(getApplicationContext(), TeacherRequestLeave.class));
//                }
//                else{
//                    Toast.makeText(getApplicationContext(),"Failed", Toast.LENGTH_LONG).show();
//                }
//            }


//            if(method.equalsIgnoreCase("teacher_reject_outpass_request_from_students"))
//            {
//                String status=jo.getString("status");
//                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
//                if(status.equalsIgnoreCase("success"))
//                {
//                    Toast.makeText(getApplicationContext()," Rejected!", Toast.LENGTH_LONG).show();
//                    startActivity(new Intent(getApplicationContext(), TeacherViewOutpass.class));
//                }
//                else{
//                    Toast.makeText(getApplicationContext(),"Rejeceted", Toast.LENGTH_LONG).show();
//                }
//            }




        }catch (Exception e)
        {
            // TODO: handle exception

            Toast.makeText(getApplicationContext(),e.toString(), Toast.LENGTH_LONG).show();
        }



    }
}