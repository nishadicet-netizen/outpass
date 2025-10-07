package com.example.myapplication;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

public class ViewMessAmount extends AppCompatActivity implements JsonResponse, AdapterView.OnItemClickListener {

    ListView l1;
    String[] value,date,amount,formonth,rid;
    public  static String req_id,amt;
    SharedPreferences sh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_mess_amount);


        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        l1=findViewById(R.id.stmasters);
        l1.setOnItemClickListener(this);




        JsonReq JR = new JsonReq();
        JR.json_response = (JsonResponse) ViewMessAmount.this;
        String q = "/viewmess_amount?lid="+sh.getString("logid","");
        q = q.replace(" ", "%20");
        JR.execute(q);
    }

    @Override
    public void response(JSONObject jo) {

        try {

            String method = jo.getString("method");
            Log.d("pearl", method);

            if (method.equalsIgnoreCase("viewmess_amount")) {
                String status = jo.getString("status");
                if (status.equalsIgnoreCase("success")) {
//                    Toast.makeText(getApplicationContext(), "test", Toast.LENGTH_LONG).show();

                    JSONArray ja1 = (JSONArray) jo.getJSONArray("data");

                    value = new String[ja1.length()];
                    amount = new String[ja1.length()];
                    date= new String[ja1.length()];
                    formonth= new String[ja1.length()];
                    rid= new String[ja1.length()];



                    for (int i = 0; i < ja1.length(); i++) {


                        rid[i] = ja1.getJSONObject(i).getString("request_id");
                        amount[i] = ja1.getJSONObject(i).getString("amount");
                        date[i] = ja1.getJSONObject(i).getString("date");
                        formonth[i] = ja1.getJSONObject(i).getString("formonth");


                        value[i] = "Your Mess Amount is " + amount[i]+" for " + formonth[i] + " Months" +"\nDate : " + date[i];
                    }
                    ArrayAdapter<String> ar = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_list_item_1, value);
                    l1.setAdapter(ar);

//                    CustomUser a = new CustomUser(this, name, num);
//                    l1.setAdapter(a);
                } else  if (status.equalsIgnoreCase("failed")) {
                    Toast.makeText(getApplicationContext(), "No data, found!", Toast.LENGTH_SHORT).show();
                }
            }

        }
        catch (Exception e) {
            // TODO: handle exception
            e.printStackTrace();
            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_SHORT).show();
        }


    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

        amt=amount[i];
        req_id=rid[i];
        final CharSequence[] items = {"Make Payment", "Cancel"};

        AlertDialog.Builder builder = new AlertDialog.Builder(ViewMessAmount.this);
        // builder.setTitle("Add Photo!");
        builder.setItems(items, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int item) {

                if (items[item].equals("Make Payment")) {


                    startActivity(new Intent(getApplicationContext(),MessPayment.class));

                }

                else if (items[item].equals("Cancel")) {
                    dialog.dismiss();
                }

            }

        });
        builder.show();
    }
}