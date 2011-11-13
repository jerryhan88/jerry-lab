import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.Insets;
import java.awt.Panel;
import java.awt.TextArea;
import java.awt.TextField;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;

public class noticePanel extends JPanel implements ActionListener, Runnable {
	private static final long serialVersionUID = 1L;
	JPanel t_p = new JPanel();
	Panel notice_p = new Panel();
	Panel typing_p = new Panel();
	
	JLabel t;
	TextArea noticeArea = new TextArea(20, 50);
	TextField typingField = new TextField(50);

	Socket s; // java.net.Socket
	PrintWriter pw; // java.io.PrintWriter
	BufferedReader br; // java.io.BufferedReader
	String str1;

	public noticePanel(String ip, int port) {
		this.setLayout(new BorderLayout());
		t_p.setLayout(new BorderLayout());
		t_p.setBorder(new EmptyBorder(new Insets(5, 10, 5, 5)));
		t_p.setBackground(new Color(64, 117, 180));
		t = new JLabel("Real time message");
		t.setFont(new Font("Times New Roman", Font.BOLD, 40));
		t.setForeground(new Color(255, 255, 255));
		t_p.add(t, BorderLayout.WEST);		
		
		
		System.out.println(this.getClass().getName() + "1. Start-->");
		notice_p.setLayout(new BorderLayout());
		typing_p.setLayout(new BorderLayout());
		
		this.add(t_p, BorderLayout.NORTH);
		this.add(notice_p, BorderLayout.CENTER);
		this.add(typing_p, BorderLayout.SOUTH);
		notice_p.add(noticeArea, BorderLayout.CENTER);
		typing_p.add(typingField, BorderLayout.CENTER);
		this.typingField.addActionListener(this);
		this.noticeArea.setEditable(false);
		this.typingField.requestFocus();
		
		
		//NOTE   Don't have to do
		noticeArea.append("---------------------------------------------------" + "\n");
		noticeArea.append(" 20111113 10:23" + "\n");
		noticeArea.append("	긴급발주 동희산업(주)" + "\n");
		noticeArea.append("---------------------------------------------------" + "\n");
		noticeArea.append(" 20111113 14:21" + "\n");
		noticeArea.append("	23가 2323차량 배송지연" + "\n");
		noticeArea.append("---------------------------------------------------" + "\n");
		
		try {
			s = new Socket(ip, port);
			System.out.println("success!!");
			
		} catch (Exception e) {
			System.out.println("소켓 생성 실패!!");
		}
		System.out.println(this.getClass().getName() + "2. Socket-->");
	}

	public void actionPerformed(ActionEvent e) {
		this.typingField.requestFocus();
		String strs = this.typingField.getText();
		pw.println(strs);
		this.typingField.setText("");
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
				this.noticeArea.append(str1 + "\n");
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