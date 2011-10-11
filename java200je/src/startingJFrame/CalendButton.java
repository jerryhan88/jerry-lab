package startingJFrame;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import javax.swing.ImageIcon;
import javax.swing.JButton;

public class CalendButton extends JButton {
	private static final long serialVersionUID = 1L;

	private String[] cals = { "일", "월", "화", "수", "목", "금", "토" };
	public static final int WIDTH = 50;
	private int width = WIDTH;
	private int height = WIDTH;
	private int imageNum = 0;
	private Color backColor;
	private Color foreColor;

	private Font f;

	public CalendButton(int imageNum) {
		this.imageNum = imageNum;
		if (imageNum < 0) {
			switch (imageNum) {
			case -1:
				this.setText(this.cals[0]);
				break;
			case -2:
				this.setText(this.cals[1]);
				break;
			case -3:
				this.setText(this.cals[2]);
				break;
			case -4:
				this.setText(this.cals[3]);
				break;
			case -5:
				this.setText(this.cals[4]);
				break;
			case -6:
				this.setText(this.cals[5]);
				break;
			case -7:
				this.setText(this.cals[6]);
				break;
			}
		}

		init();
	}

	public CalendButton() {
		this.imageNum = 0;
		init();
	}

	public void init() {
		this.backColor = new Color(255, 255, 255);
		this.foreColor = new Color(0, 0, 0);
		this.f = new Font("Sherif", Font.BOLD, 24);
		this.setBackground(this.backColor);
		this.setForeground(this.foreColor);
		this.setFont(this.f);
		if (imageNum == 0) {
			this.setText("");
		}

		this.setPreferredSize(new Dimension(width, height));
		this.addMouseListener(new MyMouseHandling());
	}

	public void reInit(Color bc, Color fc, Font f) {
		this.setBackground(bc);
		this.setForeground(fc);
		this.setFont(f);
	}

	public void reInit(Color bc, Color fc) {
		this.setBackground(bc);
		this.setForeground(fc);
	}

	public class MyMouseHandling extends MouseAdapter {
		String str = "";
		String imageNums = "image/s0.gif";

		public void mousePressed(MouseEvent e) {
			str = CalendButton.this.getText();
			if (!str.equals("")) {
				ImageIcon icon = new ImageIcon(imageNums);
				CalendButton.this.setIcon(icon);
				CalendButton.this.updateUI();
			}
		}

		public void mouseReleased(MouseEvent e) {
			CalendButton.this.setIcon(null);
			CalendButton.this.setText(str);
			CalendButton.this.updateUI();
		}
	}
}
