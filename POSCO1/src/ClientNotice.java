

	import java.awt.*;
	import java.awt.event.*;
	import javax.swing.*;
	import java.io.*;
	import java.net.*;

	public class ClientNotice extends JPanel implements ActionListener,Runnable {
	  private static final long serialVersionUID=122454214237L;//JAVA5
	  JFrame mainf;
	  Panel panel1 = new Panel();
	  Panel panel2 = new Panel();
	  TextArea textArea1 = new TextArea(20, 50);
	  TextField textField1 = new TextField(50);
	  Socket s;          //java.net.Socket
	  PrintWriter pw;     //java.io.PrintWriter
	  BufferedReader br;  //java.io.BufferedReader
	  String str1;
	  public ClientNotice(JFrame mainf, String ip, int port) {//Construct the JPanel
	    this.mainf=mainf;
	    System.out.println(this.getClass().getName()+"1. Start-->");
	    inits();
		try{
			s=new Socket(ip,port);
		}catch(Exception e){
			System.out.println("家南 积己 角菩!!");
		}
		System.out.println(this.getClass().getName()+"2. Socket-->");
	  }
	  /**Component initialization*/
	  private void inits()  {
		mainf.setTitle(this.getClass().getName());
	    this.setSize(new Dimension(400, 300));
		this.setLayout(new BorderLayout());
	    panel1.setLayout(new BorderLayout());
	    panel2.setLayout(new BorderLayout());
	    this.add(panel1, BorderLayout.CENTER);
		this.add(panel2,  BorderLayout.SOUTH);
	    panel1.add(textArea1, BorderLayout.CENTER);
	    panel2.add(textField1, BorderLayout.CENTER);
	    this.textField1.addActionListener(this);
	    this.textArea1.setEditable(false);
		this.textField1.requestFocus();
	  }
	  public void actionPerformed(ActionEvent e) {
		this.textField1.requestFocus();
	    String strs=this.textField1.getText();
	    pw.println(strs);
	    this.textField1.setText("");
	  }
	  public void giveAndTake(){
	    try{
	      System.out.println(this.getClass().getName()+"3. InputOutput-->");
	      pw = new PrintWriter(s.getOutputStream(),true);
	      br = new BufferedReader(new InputStreamReader(s.getInputStream()));
	      Thread ctr=new Thread(this);
	      ctr.start();
	    }catch(Exception e)
	    {
	        e.getMessage();
	    }
	  }
	  public void run(){
	      try{
			  System.out.println(this.getClass().getName()+"4. run-->");
	          br=new BufferedReader(new InputStreamReader(s.getInputStream()));
	          while((str1=br.readLine())!=null){
	            this.textArea1.append(str1+"\n");//
	          }
	      }catch(Exception ex){
	          ex.printStackTrace();
	      }finally{
	        try{s.close();}catch(Exception ea){ea.getMessage();}
	      }
	    }
	}

