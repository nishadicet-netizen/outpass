package com.example.myapplication;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

public class TeacherViewLeaveRequestFromStudent extends AppCompatActivity implements JsonResponse,AdapterView.OnItemClickListener {

    ListView lv1;
    Button b1;
    String request,date,reason,duration;
    String[] dates,reasons,durations,leave_id,val,statuss,course_name,first_name,last_name;
    public static String leave_ids,statusss;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_teacher_view_leave_request_from_student);

        lv1=(ListView)findViewById(R.id.lv1);
        lv1.setOnItemClickListener(this);



        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) TeacherViewLeaveRequestFromStudent.this;
        String q = "/teacher_view_leave_request_from_students";
        q=q.replace(" ","%20");
        JR.execute(q);
    }



    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method=jo.getString("method");
            if(method.equalsIgnoreCase("teacher_view_leave_request_from_students")){
                String status=jo.getString("status");
                Log.d("pearl",status);
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_SHORT).show();
                if(status.equalsIgnoreCase("success")){

                    JSONArray ja1=(JSONArray)jo.getJSONArray("data");

                    leave_id=new String[ja1.length()];
                    dates=new String[ja1.length()];
                    reasons=new String[ja1.length()];
                    durations=new String[ja1.length()];

                    statuss=new String[ja1.length()];
                    first_name=new String[ja1.length()];
                    last_name=new String[ja1.length()];
                    course_name=new String[ja1.length()];




                    val=new String[ja1.length()];



                    for(int i = 0;i<ja1.length();i++)
                    {


                        leave_id[i]=ja1.getJSONObject(i).getString("leave_id");
                        dates[i]=ja1.getJSONObject(i).getString("date");
                        reasons[i]=ja1.getJSONObject(i).getString("reason");
                        durations[i]=ja1.getJSONObject(i).getString("duration");


                        statuss[i]=ja1.getJSONObject(i).getString("status");
                        first_name[i]=ja1.getJSONObject(i).getString("first_name");
                        last_name[i]=ja1.getJSONObject(i).getString("last_name");
                        course_name[i]=ja1.getJSONObject(i).getString("course_name");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i]="FirstName: "+first_name[i]+"\nLastName: "+last_name[i]+"\nCourse: "+course_name[i]+"\nReason: "+reasons[i]+"\nDate:  "+dates[i]+"\nDuration:  "+durations[i]+"\nStatus:  "+statuss[i];


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

            if(method.equalsIgnoreCase("teacher_approve_leave_request_from_students"))
            {
                String status=jo.getString("status");
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
                if(status.equalsIgnoreCase("success"))
                {
                    Toast.makeText(getApplicationContext()," Submitted!", Toast.LENGTH_LONG).show();
                    startActivity(new Intent(getApplicationContext(), TeacherViewLeaveRequestFromStudent.class));
                }
                else{
                    Toast.makeText(getApplicationContext(),"Failed", Toast.LENGTH_LONG).show();
                }
            }
            if(method.equalsIgnoreCase("teacher_reject_leave_request_from_students"))
            {
                String status=jo.getString("status");
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
                if(status.equalsIgnoreCase("success"))
                {
                    Toast.makeText(getApplicationContext()," Rejected!", Toast.LENGTH_LONG).show();
                    startActivity(new Intent(getApplicationContext(), TeacherViewLeaveRequestFromStudent.class));
                }
                else{
                    Toast.makeText(getApplicationContext(),"Rejeceted", Toast.LENGTH_LONG).show();
                }
            }




        }catch (Exception e)
        {
            // TODO: handle exception

            Toast.makeText(getApplicationContext(),e.toString(), Toast.LENGTH_LONG).show();
        }



    }



    public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
        // TODO Auto-generated method stub
        leave_ids=leave_id[arg2];
        statusss=statuss[arg2];
        if (statusss.equals("pending")) {


            final CharSequence[] items = {"Accept","Reject", "Cancel"};

            AlertDialog.Builder builder = new AlertDialog.Builder(TeacherViewLeaveRequestFromStudent.this);

            // builder.setTitle("Add Photo!");
            builder.setItems(items, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int item) {
                    if (items[item].equals("Accept")) {
                        JsonReq JR=new JsonReq();
                        JR.json_response=(JsonResponse) TeacherViewLeaveRequestFromStudent.this;
                        String q = "/teacher_approve_leave_request_from_students?leave_id="+leave_ids;
                        q=q.replace(" ","%20");
                        JR.execute(q);

                    }
                    else if (items[item].equals("Reject")) {
                        JsonReq JR=new JsonReq();
                        JR.json_response=(JsonResponse) TeacherViewLeaveRequestFromStudent.this;
                        String q = "/teacher_reject_leave_request_from_students?leave_id="+leave_ids;
                        q=q.replace(" ","%20");
                        JR.execute(q);
                    }
                    else if (items[item].equals("Cancel")) {
                        dialog.dismiss();
                    }
                }

            });
            builder.show();
        }
//	Intent i = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        //startActivityForResult(i, GALLERY_CODE);
    }
}