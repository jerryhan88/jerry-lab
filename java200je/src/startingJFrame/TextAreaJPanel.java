package startingJFrame;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;

public class TextAreaJPanel extends JPanel {
	private static final long serialVersionUID = 1L;
	
	JPanel northp = new JPanel();
	JPanel eastp = new JPanel();
	JPanel cp = new JPanel();
	JPanel ecp = new JPanel();
	
	JLabel titlelb = new JLabel("", JLabel.CENTER);
	JLabel jLabel1 = new JLabel("", JLabel.CENTER);
	
	JButton jButton3 = new JButton("Add");
	JButton jButton4 = new JButton("Copy");
	JButton jButton2 = new JButton("Clear");
	JButton jButton1 = new JButton("Label Change");
	JScrollPane jScrollPane1 = new JScrollPane();
	JTextArea jTextArea1 = new JTextArea(10,60);
	JTextField jTextField1 = new JTextField(60);
	public TextAreaJPanel() {
		inits();
	}
	void inits() {
		this.setLayout(new BorderLayout());
		this.add(northp, BorderLayout.NORTH);
		this.add(eastp, BorderLayout.EAST);
		this.add(cp, BorderLayout.CENTER);
		northp.setLayout(new BorderLayout());
		eastp.setLayout(new BorderLayout());
		cp.setLayout(new BorderLayout());
		cp.setBorder(new TitledBorder(""));
		eastp.setBorder(new TitledBorder(""));
		
		jLabel1.setFont(new java.awt.Font("Arial", 1, 15));
		jLabel1.setToolTipText("JLabel Tooltip tests");
		jLabel1.setText("Input Texts");
		titlelb.setFont(new java.awt.Font("Arial", Font.BOLD, 20));
		titlelb.setBorder(new TitledBorder("Title"));
		titlelb.setText("TextArea Test");
		northp.add(titlelb);
		
		eastp.add(ecp, BorderLayout.CENTER);
		ecp.setPreferredSize(new Dimension(100, 35));
		ecp.add(jButton3);
		ecp.add(jButton4);
		ecp.add(jButton2);
		ecp.add(jButton1);
		cp.add(jScrollPane1, "Center");
		cp.add(jTextField1, "South");
		cp.add(jLabel1, "West");
		jScrollPane1.getViewport().add(jTextArea1);
		jTextArea1.setWrapStyleWord(true);
		jTextArea1.setLineWrap(true);
		this.jTextArea1.setCaretColor(new Color(255,0,0));
		this.jTextArea1.setSelectedTextColor(new Color(0,0,255));
		addListener();
	}
	
	public void addListener() {
		
	}
}
