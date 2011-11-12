import java.awt.BorderLayout;
import java.awt.Panel;
import java.awt.TextArea;
import java.awt.TextField;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

import javax.swing.JPanel;

public class noticePanel extends JPanel implements ActionListener, Runnable {
	private static final long serialVersionUID = 1L;
	Panel panel1 = new Panel();
	Panel panel2 = new Panel();

	TextArea textArea1 = new TextArea(20, 50);
	TextField textField1 = new TextField(50);

	Socket s; // java.net.Socket
	PrintWriter pw; // java.io.PrintWriter
	BufferedReader br; // java.io.BufferedReader
	String str1;

	public noticePanel(int ppx, int ppy, int psx, int psy, String ip, int port) {
		System.out.println(this.getClass().getName() + "1. Start-->");
		this.setLayout(new BorderLayout());
		this.setBounds(ppx, ppy, psx, psy);
		
		panel1.setLayout(new BorderLayout());
		panel2.setLayout(new BorderLayout());
		this.add(panel1, BorderLayout.CENTER);
		this.add(panel2, BorderLayout.SOUTH);
		panel1.add(textArea1, BorderLayout.CENTER);
		panel2.add(textField1, BorderLayout.CENTER);
		this.textField1.addActionListener(this);
		this.textArea1.setEditable(false);
		this.textField1.requestFocus();
		try {
			s = new Socket(ip, port);
			System.out.println("success!!");
			
		} catch (Exception e) {
			System.out.println("家南 积己 角菩!!");
		}
		System.out.println(this.getClass().getName() + "2. Socket-->");
	}

	public void actionPerformed(ActionEvent e) {
		this.textField1.requestFocus();
		String strs = this.textField1.getText();
		pw.println(strs);
		this.textField1.setText("");
	}

	public void giveAndTake() {
		try {
			System.out.println(this.getClass().getName() + "3. InputOutput-->");
			pw = new PrintWriter(s.getOutputStream(), true);
			br = new BufferedReader(new InputStreamReader(s.getInputStream()));
			Thread ctr = new Thread(this);
			ctr.start();
		} catch (Exception e) {
			e.getMessage();
		}
	}

	public void run() {
		try {
			System.out.println(this.getClass().getName() + "4. run-->");
			br = new BufferedReader(new InputStreamReader(s.getInputStream()));
			while ((str1 = br.readLine()) != null) {
				this.textArea1.append(str1 + "\n");//
			}
		} catch (Exception ex) {
			ex.printStackTrace();
		} finally {
			try {
				s.close();
			} catch (Exception ea) {
				ea.getMessage();
			}
		}
	}
}