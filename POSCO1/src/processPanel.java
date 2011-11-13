import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.Insets;

import java.awt.Container;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;

public class processPanel extends JPanel {
	private static final long serialVersionUID = 1L;
	processDrawing graph;
	JPanel t_p = new JPanel();
	JPanel m_p = new JPanel();
	JLabel t;
	
	JButton recBtn;
	JButton circleBtn;
	JButton arrowBtn;
	JButton deliveryBtn;
	JButton xBtn;
	JButton moneyBtn;
	
	public processPanel() {
		this.setLayout(new BorderLayout());
		
		t_p.setLayout(new BorderLayout());
		t_p.setBorder(new EmptyBorder(new Insets(5, 10, 5, 5)));
		t_p.setBackground(new Color(64, 117, 180));
		t = new JLabel("My Product");
		t.setFont(new Font("Times New Roman", Font.BOLD, 40));
		t.setForeground(new Color(255, 255, 255));
		t_p.add(t, BorderLayout.WEST);
		this.add(t_p, BorderLayout.NORTH);
		
		m_p.setLayout(new GridLayout(6, 1));
//		m_p.setBackground(new Color(20, 117, 180));
		
		ImageIcon recBtn_img = new ImageIcon("pic//recBtn.png");
		recBtn = new JButton(recBtn_img);
		recBtn.setBorderPainted(false);
		
		ImageIcon circleBtn_img = new ImageIcon("pic//circleBtn.png");
		circleBtn = new JButton(circleBtn_img);
		circleBtn.setBorderPainted(false);
		
		ImageIcon arrowBtn_img = new ImageIcon("pic//arrowBtn.png");
		arrowBtn = new JButton(arrowBtn_img);
		arrowBtn.setBorderPainted(false);
		
		ImageIcon deliveryBtn_img = new ImageIcon("pic//deliveryBtn.png");
		deliveryBtn = new JButton(deliveryBtn_img);
		deliveryBtn.setBorderPainted(false);
		
		ImageIcon xBtn_img = new ImageIcon("pic//xBtn.png");
		xBtn = new JButton(xBtn_img);
		xBtn.setBorderPainted(false);
		
		ImageIcon moneyBtn_img = new ImageIcon("pic//moneyBtn.png");
		moneyBtn = new JButton(moneyBtn_img);
		moneyBtn.setBorderPainted(false);
		
		m_p.add(recBtn);
		m_p.add(circleBtn);
		m_p.add(arrowBtn);
		m_p.add(deliveryBtn);
		m_p.add(xBtn);
		m_p.add(moneyBtn);
		this.add(m_p, BorderLayout.WEST);
		
		graph = new processDrawing();
		this.add("Center", graph);
		
	}
}
