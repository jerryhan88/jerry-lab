import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Label;
import java.awt.TextField;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class LFrame extends JFrame {
	private static final long serialVersionUID = 1L;
	Label t_lb;
	Label id_lb;
	Label pw_lb;
	JButton signBtn;
	JTextField id_t;

	public LFrame() {
		super("POSCO");
		setBounds(100, 50, 1024, 768);
		JPanel m_p = (JPanel) getContentPane();
		m_p.setLayout(null);

		t_lb = new Label("POSCO SYSTEM", Label.CENTER);
		t_lb.setBounds(150, 100, 700, 150);
		t_lb.setBackground(new Color(64, 117, 180));
		t_lb.setFont(new Font("Times New Roman", Font.BOLD, 40));
		t_lb.setForeground(new Color(255, 255, 255));
		m_p.add(t_lb);

		id_lb = new Label("ID", Label.CENTER);
		id_lb.setBounds(560, 350, 120, 30);
		id_lb.setBackground(new Color(64, 117, 180));
		id_lb.setFont(new Font("Times New Roman", Font.BOLD, 30));
		id_lb.setForeground(new Color(255, 255, 255));
		m_p.add(id_lb);
		id_t = new JTextField("200727196");
		id_t.setBounds(690,350,150,30);
		m_p.add(id_t);

		pw_lb = new Label("PW", Label.CENTER);
		pw_lb.setBounds(560, 400, 120, 30);
		pw_lb.setBackground(new Color(64, 117, 180));
		pw_lb.setFont(new Font("Times New Roman", Font.BOLD, 30));
		pw_lb.setForeground(new Color(255, 255, 255));
		m_p.add(pw_lb);

		TextField pwinput = new TextField(30);

		signBtn = new JButton("Sign in");
		signBtn.setBackground(null);
		signBtn.setFont(new Font("Times New Roman", Font.BOLD, 20));
		signBtn.setForeground(new Color(0));
		signBtn.setBounds(650, 460, 100, 30);
		m_p.add(signBtn);

		// JButton signuplb = new JButton("Sign up a new POSCO Account");

		SimplePanel co_panel = new SimplePanel();
		co_panel.setBounds(50, 280, 652, 415);
		m_p.add(co_panel);

		/*
		 * 
		 * 
		 * JButton helplb = new JButton("Can't access your account?");
		 * 
		 * 
		 * 
		 * 
		 * 
		 * 
		 * 
		 * 
		 * signuplb.setBackground(new java.awt.Color(-20)); this.add(signuplb);
		 * signuplb.setFont(new java.awt.Font("Times New Roman",
		 * Font.LAYOUT_LEFT_TO_RIGHT, 20)); signuplb.setForeground(new
		 * java.awt.Color(0)); signuplb.setBounds(550, 530, 300, 30);
		 * 
		 * helplb.setBackground(new java.awt.Color(-20)); this.add(helplb);
		 * helplb.setFont(new java.awt.Font("Times New Roman",
		 * Font.LAYOUT_LEFT_TO_RIGHT, 20)); helplb.setForeground(new
		 * java.awt.Color(0)); helplb.setBounds(550, 570, 300, 30);
		 * 
		 * this.add(idinput); idinput.setBounds(705,400,200,20);
		 * 
		 * this.add(pwinput); pwinput.setBounds(705,430,200,20);
		 */

		WindowListener wndCloser = new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		};

		addWindowListener(wndCloser);
		setVisible(true);
	}

	public static void main(String[] args) {
		new LFrame();
	}
}

class SimplePanel extends JPanel {
	private static final long serialVersionUID = 1L;

	private static ImageIcon co = new ImageIcon("pic//cowork.png");

	public Dimension getPreferredSize() {
		return new Dimension(200, 200);
	}

	public Dimension getMinimumSize() {
		return new Dimension(40, 40);
	}

	public void paintComponent(Graphics g) {
		// g.setColor(Color.black);
		// Dimension sz = getSize();
		// g.drawLine(0, 0, sz.width, sz.height);
		// g.drawLine(sz.width, 0, 0, sz.height);

		co.paintIcon(this, g, 100, 100);
	}
}