package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONObject;

import java.util.Calendar;

public class RoomPayment extends AppCompatActivity implements JsonResponse, View.OnClickListener {

    EditText e1,e2,e3,e4;
    String amount,acno,cvv,exp;
    private int mYear, mMonth, mDay, mHour, mMinute;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room_payment);

        e1=findViewById(R.id.amount);
        e2=findViewById(R.id.acno);
        e3=findViewById(R.id.cvv);
        e4=findViewById(R.id.expdate);
        e4.setOnClickListener(this);
        e1.setText(ViewRoomAmount.amt);

        Button b1 = findViewById(R.id.button5);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amount=e1.getText().toString();
                acno=e2.getText().toString();
                cvv=e3.getText().toString();
                exp=e4.getText().toString();

                if (amount.equalsIgnoreCase("")) {
                    e1.setError("Enter Amount");
                    e1.setFocusable(true);
                } else if (acno.equalsIgnoreCase("") || acno.length()!=16) {
                    e2.setError("Enter 16 digit account number");
                    e2.setFocusable(true);
                }
                else if (cvv.equalsIgnoreCase("") || cvv.length()!=3) {
                    e3.setError("Enter your Cvv");
                    e3.setFocusable(true);
                }
                else if (exp.equalsIgnoreCase("") ) {
                    e4.setError("Enter Expiry Date ");
                    e4.setFocusable(true);
                }else {

                    JsonReq JR = new JsonReq();
                    JR.json_response = (JsonResponse) RoomPayment.this;
                    String q = "/roompayment?amount=" + amount + "&rid=" + ViewRoomAmount.req_id;
                    q = q.replace(" ", "%20");
                    JR.execute(q);
                }
            }
        });
    }

    @Override
    public void response(JSONObject jo) {
        try {
            String status = jo.getString("status");
            Log.d("pearl", status);

            if (status.equalsIgnoreCase("success")) {

                Toast.makeText(getApplicationContext(), "Payment Successful", Toast.LENGTH_SHORT).show();
                startActivity(new Intent(getApplicationContext(), StudentHome.class));

            } else  if (status.equalsIgnoreCase("samemonth")) {

                Toast.makeText(getApplicationContext(), "You Have Already Paid This Month Payment! ", Toast.LENGTH_SHORT).show();


            }
        }
        catch (Exception e) {
            // TODO: handle exception

            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onClick(View view) {
        final Calendar c = Calendar.getInstance();
        mYear = c.get(Calendar.YEAR);
        mMonth = c.get(Calendar.MONTH);
        mDay = c.get(Calendar.DAY_OF_MONTH);


        DatePickerDialog datePickerDialog = new DatePickerDialog(this,
                new DatePickerDialog.OnDateSetListener() {

                    @Override
                    public void onDateSet(DatePicker view, int year,
                                          int monthOfYear, int dayOfMonth) {

                        e4.setText(dayOfMonth + "-" + (monthOfYear + 1) + "-" + year);

                    }
                }, mYear, mMonth, mDay);
        datePickerDialog.show();
    }
}