package com.example.myapplication;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

import com.squareup.picasso.Picasso;

public class StudentViewSanctionedQrForOutpass extends AppCompatActivity {
    String image;
    ImageView im;
    SharedPreferences sh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_view_sanctioned_qr_for_outpass);

        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        im=(ImageView) findViewById(R.id.imageView);
        image=StudentRequestOutpass.qrs;

        String pth = "http://"+sh.getString("ip", "")+"/"+image;
        pth = pth.replace("~", "");
//	       Toast.makeText(context, pth, Toast.LENGTH_LONG).show();

        Log.d("-------------", pth);



        Picasso.with(getApplicationContext())
                .load(pth)
                .placeholder(R.drawable.ic_launcher_background)
                .error(R.drawable.ic_launcher_background).into(im);

//        Custimage ci=new Custimage(StudentViewSanctionedQrForOutpass.this,image);

//        lv1.setAdapter(ci);
    }
}