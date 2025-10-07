package com.example.myapplication;

import android.app.Activity;
import android.app.DatePickerDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Calendar;

public class StudentRequestLeave extends AppCompatActivity implements JsonResponse {

    ListView lv1;
    Button b1;
    String request,date,reason,duration;
    String[] dates,reasons,durations,leave_id,val,statuss;

    EditText e1,e2,e3;
    DatePickerDialog datePickerDialog;
    SharedPreferences sh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_request_leave);





        lv1=(ListView)findViewById(R.id.lv1);
//
        e1=(EditText)findViewById(R.id.etreason);
        e2=(EditText)findViewById(R.id.etdate);
        e3=(EditText)findViewById(R.id.etduration);

        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());




        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) StudentRequestLeave.this;
        String q = "/student_view_leave_request?login_id="+Login.logid;
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
                datePickerDialog = new DatePickerDialog(StudentRequestLeave.this,
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





        b1=(Button)findViewById(R.id.btsend);
        b1.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub
                reason=e1.getText().toString();
                date=e2.getText().toString();
                duration=e3.getText().toString();
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
                else if(duration.equalsIgnoreCase(""))
                {
                    e3.setError("No value for No.Of Days");
                    e3.setFocusable(true);
                }
                else{
                    JsonReq JR=new JsonReq();
                    JR.json_response=(JsonResponse) StudentRequestLeave.this;
                    String q = "/student_send_leave_request?login_id="+Login.logid+"&reason="+reason+"&leave_date="+date+"&nodays="+duration;
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
            if(method.equalsIgnoreCase("student_view_leave_request")){
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
//                    company_name=new String[ja1.length()];
//                    product_name=new String[ja1.length()];




                    val=new String[ja1.length()];



                    for(int i = 0;i<ja1.length();i++)
                    {


                        leave_id[i]=ja1.getJSONObject(i).getString("leave_id");
                        dates[i]=ja1.getJSONObject(i).getString("date");
                        reasons[i]=ja1.getJSONObject(i).getString("reason");
                        durations[i]=ja1.getJSONObject(i).getString("duration");


                        statuss[i]=ja1.getJSONObject(i).getString("status");
//                        product_name[i]=ja1.getJSONObject(i).getString("product_name");
//                        place[i]=ja1.getJSONObject(i).getString("place");


//                        Toast.makeText(getApplicationContext(),val[i], Toast.LENGTH_SHORT).show();
                        val[i]="Reason: "+reasons[i]+"\nDate:  "+dates[i]+"\nDuration:  "+durations[i]+"\nStatus:  "+statuss[i];


                    }
                    ArrayAdapter<String> ar=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,val);
                    lv1.setAdapter(ar);



                }

                else {
                    Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();

                }
            }


            if(method.equalsIgnoreCase("student_send_leave_request"))
            {
                String status=jo.getString("status");
                Toast.makeText(getApplicationContext(),status, Toast.LENGTH_LONG).show();
                if(status.equalsIgnoreCase("success"))
                {
                    Toast.makeText(getApplicationContext()," Submitted!", Toast.LENGTH_LONG).show();
                    startActivity(new Intent(getApplicationContext(), TeacherRequestLeave.class));
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