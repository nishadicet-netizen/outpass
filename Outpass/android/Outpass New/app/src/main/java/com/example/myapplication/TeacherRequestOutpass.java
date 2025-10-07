package com.example.myapplication;

import android.app.Activity;
import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TimePicker;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Calendar;

public class TeacherRequestOutpass extends AppCompatActivity implements JsonResponse, AdapterView.OnItemClickListener {
    ListView lv1;
    Button b1;
    String request,date,reason,duration,time;
    String[] dates,reasons,times,pass_id,val,statuss,qr;
    public static String statusss,pass_ids,qrs;

    EditText e1,e2,e3;
    DatePickerDialog datePickerDialog;
    SharedPreferences sh;
    TimePickerDialog timePickerDialog;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_teacher_request_outpass);



        lv1=(ListView)findViewById(R.id.lv1);
        lv1.setOnItemClickListener(this);
//
        e1=(EditText)findViewById(R.id.etreason);
        e2=(EditText)findViewById(R.id.etdate);
        e3=(EditText)findViewById(R.id.ettime);

        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());




        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) TeacherRequestOutpass.this;
        String q = "/teacher_view_outpass_request?login_id="+Login.logid;
        q=q.replace(" ","%20");
        JR.execute(q);




        e2.setOnClickListener(new View.OnClickListener() {


            @Override
            public void onClick(View v) {
                // calender class's instance and get current date , month and year from calender
                final Calendar c = Calendar.getInstance();
                int mYear = c.get(Calendar.YEAR); // current year
                int mMonth = c.get(Calendar.MONTH); // current month
                int mDay = c.get(Calendar.DAY_OF_MONTH); // current day
                // date picker dialog
                datePickerDialog = new DatePickerDialog(TeacherRequestOutpass.this,
                        new DatePickerDialog.OnDateSetListener() {

                            @Override
                            public void onDateSet(DatePicker view, int year,
                                                  int monthOfYear, int dayOfMonth) {
                                String month = "", day_temp = "";
                                // set day of month , month and year value in the edit text
                                if (dayOfMonth < 10)
                                    day_temp = "0" + String.valueOf(dayOfMonth);
                                else
                                    day_temp = String.valueOf(dayOfMonth);
                                monthOfYear += 1;
                                if (monthOfYear < 10)
                                    month = "0" + monthOfYear;
                                else
                                    month = String.valueOf(monthOfYear);

                                e2.setText(year + "-" + month + "-" + day_temp);

                            }
                        }, mYear, mMonth, mDay);
                datePickerDialog.show();
            }
        });





        e3.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                // calender class's instance and get current date , month and year from calender

                TimePickerDialog timePickerDialog = new TimePickerDialog(TeacherRequestOutpass.this, new TimePickerDialog.OnTimeSetListener() {
                    @Override
                    public void onTimeSet(TimePicker timePicker, int hourOfDay, int minutes) {

//                        String amPm;
//                        if (hourOfDay >= 12) {
//                            amPm = "PM";
//                        } else {
//                            amPm = "AM";
//                        }
//                        e2.setText(String.format("%02d:%02d", hourOfDay, minutes) + amPm);

                        e3.setText(hourOfDay + ":" + minutes);
                    }
                }, 0, 0, false);

                timePickerDialog.show();

            }
        });



        b1=(Button)findViewById(R.id.btsend);
        b1.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub
                reason=e1.getText().toString();
                date=e2.getText().toString();
                time=e3.getText().toString();
                if(reason.equalsIgnoreCase(""))
                {
                    e1.setError("No value for Reason");
                    e1.setFocusable(true);
                }
                else if(date.equalsIgnoreCase(""))
                {
                    e2.setError("No value for Leave Date");
                    e2.setFocusable(true);
                }
                else if(time.equalsIgnoreCase(""))
                {
                    e3.setError("No value for time");
                    e3.setFocusable(true);
                }
                else{
                    JsonReq JR=new JsonReq();
                    JR.json_response=(JsonResponse)TeacherRequestOutpass.this;
                    String q = "/teacher_send_outpass_request?login_id="+Login.logid+"&reason="+reason+"&date="+date+"&time="+time;
                    q=q.replace(" ","%20");
                    JR.execute(q);
                }
            }
        });
    }







    public void response(JSONObject jo) {
        // TODO Auto-generated method stub
        try {

            String method=jo.getString("method");
            if(method.equalsIgnoreCase("teacher_view_outpass_request")){
                String status=jo.getString("status");
                Log.d("pearl",status);
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_SHORT).show();
                if(status.equalsIgnoreCase("success")){

                    JSONArray ja1=(JSONArray)jo.getJSONArray("data");

                    pass_id=new String[ja1.length()];
                    dates=new String[ja1.length()];
                    reasons=new String[ja1.length()];
                    times=new String[ja1.length()];

                    statuss=new String[ja1.length()];
                    qr=new String[ja1.length()];
//                    product_name=new String[ja1.length()];




                    val=new String[ja1.length()];



                    for(int i = 0;i<ja1.length();i++)
                    {


                        pass_id[i]=ja1.getJSONObject(i).getString("pass_id");
                        dates[i]=ja1.getJSONObject(i).getString("request_date");
                        reasons[i]=ja1.getJSONObject(i).getString("reason");
                        times[i]=ja1.getJSONObject(i).getString("request_time");


                        statuss[i]=ja1.getJSONObject(i).getString("status");
                        qr[i]=ja1.getJSONObject(i).getString("qr");
//                        place[i]=ja1.getJSONObject(i).getString("place");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i]="Reason: "+reasons[i]+"\nDate:  "+dates[i]+"\nTime:  "+times[i]+"\nStatus:  "+statuss[i];


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



    public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
        // TODO Auto-generated method stub
        pass_ids=pass_id[arg2];
        statusss=statuss[arg2];
        qrs=qr[arg2];
        if (statusss.equals("principal approved teacher outpass")) {


            final CharSequence[] items = {"View QR", "Cancel"};

            AlertDialog.Builder builder = new AlertDialog.Builder(TeacherRequestOutpass.this);

            // builder.setTitle("Add Photo!");
            builder.setItems(items, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int item) {
                    if (items[item].equals("View QR")) {

                        startActivity(new Intent(getApplicationContext(), TeacherViewSanctionedQrForOutPass.class));
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