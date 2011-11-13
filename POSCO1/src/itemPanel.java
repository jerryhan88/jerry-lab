import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Insets;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;

public class itemPanel extends JPanel {
	private static final long serialVersionUID = 1L;
	JPanel t_p = new JPanel();
	JPanel c_p = new JPanel();
	JPanel b_p = new JPanel();

	JLabel t;

	JLabel i1;
	JLabel i2;
	JLabel i3;

	
	JButton plusBtn;
	JButton minusBtn;
	JButton prevBtn;
	JButton nextBtn;
	
	public itemPanel() {
		this.setLayout(new BorderLayout());

		t_p.setLayout(new BorderLayout());
		t_p.setBorder(new EmptyBorder(new Insets(5, 10, 5, 5)));
		t_p.setBackground(new Color(64, 117, 180));
		t = new JLabel("My Product");
		t.setFont(new Font("Times New Roman", Font.BOLD, 40));
		t.setForeground(new Color(255, 255, 255));
		t_p.add(t, BorderLayout.WEST);
		this.add(t_p, BorderLayout.NORTH);

		c_p.setLayout(new GridLayout(1, 3));
		ImageIcon img1 = new ImageIcon("pic//TORX.png");
		ImageIcon img2 = new ImageIcon("pic//TORXPLUS.png");
		ImageIcon img3 = new ImageIcon("pic//TRILOBULAR.png");
		i1 = new JLabel(img1);
		i2 = new JLabel(img2);
		i3 = new JLabel(img3);
		c_p.add(i1);
		c_p.add(i2);
		c_p.add(i3);
		this.add(c_p, BorderLayout.CENTER);

		b_p.setLayout(new GridBagLayout());
		Color b_p_BC = new Color(189,207,231);
		b_p.setBackground(b_p_BC);
		
		GridBagConstraints c = new GridBagConstraints();
		
		ImageIcon plus_img = new ImageIcon("pic//+.png");
		plusBtn = new JButton(plus_img);
		c.gridx = 1;
		plusBtn.setBorderPainted(false);
		plusBtn.setBackground(b_p_BC);
		b_p.add(plusBtn, c);
		
		ImageIcon minus_img = new ImageIcon("pic//-.png");
		minusBtn = new JButton(minus_img);
		c.gridx = 2;
		minusBtn.setBorderPainted(false);
		minusBtn.setBackground(b_p_BC);
		b_p.add(minusBtn, c);
		
		for (int i = 3 ; i < 6; i++) {
			c.gridx = i;
			b_p.add(new JLabel("                                      "), c);
		} 
		
		
		ImageIcon prev_img = new ImageIcon("pic//prev.png");
		prevBtn = new JButton(prev_img);
		c.gridx = 7;
		prevBtn.setBorderPainted(false);
		prevBtn.setBackground(b_p_BC);
		b_p.add(prevBtn, c);
		
		ImageIcon next_img = new ImageIcon("pic//next.png");
		nextBtn = new JButton(next_img);
		c.gridx = 8;
		nextBtn.setBorderPainted(false);
		nextBtn.setBackground(b_p_BC);
		b_p.add(nextBtn, c);
		
		this.add(b_p, BorderLayout.SOUTH);
	}

}
