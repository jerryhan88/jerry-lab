package startingJFrame;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;

public class TextAreaJPanel2 extends JPanel implements ActionListener,
		MouseMotionListener, MouseListener, KeyListener {
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
	JTextArea jTextArea1 = new JTextArea(10, 60);
	JTextField jTextField1 = new JTextField(60);

	public TextAreaJPanel2() {
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
		ecp.add(jButton4, null);
		ecp.add(jButton2);
		ecp.add(jButton1);
		cp.add(jScrollPane1, "Center");
		cp.add(jTextField1, "South");
		cp.add(jLabel1, "West");
		jScrollPane1.getViewport().add(jTextArea1);
		jTextArea1.setWrapStyleWord(true);
		jTextArea1.setLineWrap(true);
		this.jTextArea1.setCaretColor(new Color(255, 0, 0));
		this.jTextArea1.setSelectedTextColor(new Color(0, 0, 255));
		addListener();
	}

	//
	public void addListener() {
		jButton3.addActionListener(this);
		jButton4.addActionListener(this);
		jButton2.addMouseListener(this);
		jTextField1.addKeyListener(this);
		jButton1.addMouseMotionListener(this);
		jTextField1.addMouseMotionListener(this);
		jTextArea1.addMouseMotionListener(this);
	}

	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		if (e.getSource() == jButton3) {
			jLabel1.setText(jTextArea1.getSelectedText());
		} else if (e.getSource() == jButton4) {
			jTextArea1.append(jTextField1.getText() + "\n");
			jTextField1.setText("");
		}
	}

	@Override
	public void keyPressed(KeyEvent e) {
		// TODO Auto-generated method stub
		if (e.getSource() == jTextField1) {
			if (KeyEvent.VK_ENTER == e.getKeyCode()) {
				jTextArea1.append(jTextField1.getText() + "\n");
				jTextField1.setText("");

			}
		}
	}

	public void keyReleased(KeyEvent e) {
	}

	public void keyTyped(KeyEvent arg0) {
	}

	@Override
	public void mouseClicked(MouseEvent e) {
		// TODO Auto-generated method stub
		if (e.getSource() == jButton2) {
			jTextArea1.setText("");
		}
	}

	public void mouseEntered(MouseEvent e) {
	}

	public void mouseExited(MouseEvent e) {
	}

	public void mousePressed(MouseEvent e) {
	}

	public void mouseReleased(MouseEvent arg0) {
	}

	@Override
	public void mouseDragged(MouseEvent e) {
		// TODO Auto-generated method stub
		if (e.getSource() == jTextField1) {
			jLabel1.setText(jTextField1.getSelectedText() + "\n");
		}
	}

	@Override
	public void mouseMoved(MouseEvent e) {
		// TODO Auto-generated method stub
		if (e.getSource() == jTextField1) {
			jLabel1.setText("Number of Characters: "
					+ jTextArea1.getCaretPosition());
		} else if (e.getSource() == jButton1) {
			jLabel1.setText("(x,y)=(" + e.getX() + "," + e.getY() + ")");
		}
	}
}
