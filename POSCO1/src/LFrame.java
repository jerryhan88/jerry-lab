import java.awt.Color;

import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;

public class LFrame extends JFrame implements ActionListener {
	private static final long serialVersionUID = 1L;
	JLabel t_lb;
	JLabel id_lb;
	JLabel pw_lb;
	JButton signBtn;
	JTextField id_t;

	JPasswordField pw_t;
	JButton signupBtn;
	JButton helpBtn;
	JLabel copy_r;

	public LFrame() {
		super("POSCO");
		setBounds(100, 50, 1024, 768);
		JPanel m_p = (JPanel) getContentPane();
		m_p.setLayout(null);
		Color b_color = new Color(64, 117, 180);
		Font content_f = new Font("Times New Roman", Font.BOLD, 30);
		Color f_color = new Color(255, 255, 255);
		Font btn_f = new java.awt.Font("Times New Roman",
				Font.LAYOUT_LEFT_TO_RIGHT, 20);
		Color btn_color = new Color(0);

		t_lb = new JLabel("POSCO SYSTEM", JLabel.CENTER);
		t_lb.setBounds(150, 100, 700, 150);
		t_lb.setBackground(b_color);
		t_lb.setOpaque(true);
		t_lb.setFont(new Font("Times New Roman", Font.BOLD, 40));
		t_lb.setForeground(f_color);
		m_p.add(t_lb);

		SimplePanel co_panel = new SimplePanel();
		co_panel.setBounds(50, 265, 652, 415);
		m_p.add(co_panel);

		id_lb = new JLabel("ID", JLabel.CENTER);
		id_lb.setBounds(560, 350, 120, 30);
		id_lb.setBackground(b_color);
		id_lb.setOpaque(true);
		id_lb.setFont(content_f);
		id_lb.setForeground(f_color);
		m_p.add(id_lb);
		id_t = new JTextField("200727196");
		id_t.setBounds(690, 350, 150, 30);
		m_p.add(id_t);

		pw_lb = new JLabel("PW", JLabel.CENTER);
		pw_lb.setBounds(560, 400, 120, 30);
		pw_lb.setBackground(b_color);
		pw_lb.setOpaque(true);
		pw_lb.setFont(content_f);
		pw_lb.setForeground(f_color);
		m_p.add(pw_lb);

		pw_t = new JPasswordField("1234");
		pw_t.setBounds(690, 400, 150, 30);
		m_p.add(pw_t);

		signBtn = new JButton("Sign in");
		signBtn.setBackground(null);
		signBtn.setFont(btn_f);
		signBtn.setForeground(btn_color);
		signBtn.setBounds(650, 460, 100, 30);
		m_p.add(signBtn);

		signupBtn = new JButton("Sign up a new POSCO Account");
		signupBtn.setFont(btn_f);
		signupBtn.setForeground(btn_color);
		signupBtn.setBounds(550, 530, 300, 30);
		m_p.add(signupBtn);

		helpBtn = new JButton("Can't access your account?");
		helpBtn.setFont(btn_f);
		helpBtn.setForeground(btn_color);
		helpBtn.setBounds(550, 570, 300, 30);
		m_p.add(helpBtn);

		copy_r = new JLabel(
				"Copyright 2011 HeadFirst. Pusan Univ. All right reserved.",
				JLabel.CENTER);
		copy_r.setBounds(250, 630, 520, 30);
		m_p.add(copy_r);

		WindowListener wndCloser = new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		};
		addListener();
		addWindowListener(wndCloser);
		setVisible(true);
	}

	public void addListener() {
		signBtn.addActionListener(this);
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		
		// TODO Auto-generated method stub
		if (e.getSource() == signBtn) {
			MFrame main = new MFrame();
			this.dispose();
//			System.exit(0);
		}
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
		co.paintIcon(this, g, 100, 100);
	}
}