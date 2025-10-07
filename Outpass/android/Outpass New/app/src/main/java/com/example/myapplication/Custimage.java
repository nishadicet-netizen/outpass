package com.example.myapplication;

import android.app.Activity;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.Collections;

public class Custimage extends ArrayAdapter<String>  {

	 private Activity context;       //for to get current activity context
	    SharedPreferences sh;
	private String[] post;
	private String[] date;
	private String[] statuss;
	private String image;

	
	
	 public Custimage(Activity context, String image) {
	        //constructor of this class to get the values from main_activity_class

	        super(context, R.layout.cust_images, Collections.singletonList(image));
	        this.context = context;
	        this.image = image;
//	        this.date=date;
//	        this.statuss = statuss;
//	        this.details = details;

	    }

	    @Override
	    public View getView(int position, View convertView, ViewGroup parent) {
	                 //override getView() method

	        LayoutInflater inflater = context.getLayoutInflater();
	        View listViewItem = inflater.inflate(R.layout.cust_images, null, true);
			//cust_list_view is xml file of layout created in step no.2

	        ImageView im = (ImageView) listViewItem.findViewById(R.id.imageView1);
//			TextView t=(TextView)listViewItem.findViewById(R.id.textView);
//	        TextView t1=(TextView)listViewItem.findViewById(R.id.textView1);
//	        TextView t2=(TextView)listViewItem.findViewById(R.id.textView2);
//	        TextView t3=(TextView)listViewItem.findViewById(R.id.textView3);
//	        TextView t4=(TextView)listViewItem.findViewById(R.id.textView4);


//			t.setText("Date : "+ date[position]);
//
//	        t3.setText("Status : "+statuss[position]);
//	        t4.setText("Details : "+details[position]);
	        
	        
	        
	        sh=PreferenceManager.getDefaultSharedPreferences(getContext());
	        
	       String pth = "http://"+sh.getString("ip", "")+"/"+post[position];
	       pth = pth.replace("~", "");
//	       Toast.makeText(context, pth, Toast.LENGTH_LONG).show();
	        
	        Log.d("-------------", pth);



	        Picasso.with(context)
	                .load(pth)
	                .placeholder(R.drawable.ic_launcher_background)
	                .error(R.drawable.ic_launcher_background).into(im);
	        
	        return  listViewItem;
	    }

		private TextView setText(String string) {
			// TODO Auto-generated method stub
			return null;
		}
}