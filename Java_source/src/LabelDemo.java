import java.awt.Color;
import java.awt.Font;
import java.awt.GridLayout;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;


public class LabelDemo extends JFrame {
	private static final long serialVersionUID = 1L;

	public LabelDemo() {
		super("JLabel Demo");
		setSize(600,100);
		
		JPanel content = (JPanel) getContentPane();
		content.setLayout(new GridLayout(1,4,4,4));
		
		JLabel label = new JLabel();
		label.setText("JLabel");
		label.setBackground(Color.WHITE);
		content.add(label);
		
		label = new JLabel("JLabel", SwingConstants.CENTER);
		label.setOpaque(true);
		label.setBackground(Color.WHITE);
		content.add(label);
		
		label = new JLabel("JLabel");
		label.setFont(new Font("Helvetica", Font.BOLD, 18));
		label.setOpaque(true);
		label.setBackground(Color.white);
		content.add(label);
		ImageIcon image = new ImageIcon("pic//flight.gif");
		label = new JLabel("JLabel", image, SwingConstants.RIGHT);
		label.setOpaque(true);
		label.setBackground(Color.white);
		content.add(label);
		
		
		
		setVisible(true);
	}
	
	public static void main(String[] args){
		new LabelDemo();
	}
}
