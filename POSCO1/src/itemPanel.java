import java.awt.GridLayout;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class itemPanel extends JPanel {
	private static final long serialVersionUID = 1L;

	ImageIcon img1;
	JButton btn1;

	ImageIcon img2;
	JButton btn2;

	ImageIcon img3;
	JButton btn3;

	public itemPanel(int ppx, int ppy, int psx, int psy) {
		this.setLayout(new GridLayout(1, 3));
		this.setBounds(ppx, ppy, psx, psy);
		

		img1 = new ImageIcon(
				"C:/Documents and Settings/Apple/πŸ≈¡ »≠∏È/poscoPic/TORX.png");
		img2 = new ImageIcon(
				"C:/Documents and Settings/Apple/πŸ≈¡ »≠∏È/poscoPic/TORX.png");
		img3 = new ImageIcon(
				"C:/Documents and Settings/Apple/πŸ≈¡ »≠∏È/poscoPic/TORX.png");

		btn1 = new JButton(img1);
		btn2 = new JButton(img2);
		btn3 = new JButton(img2);

		this.add(btn1);
		this.add(btn2);
		this.add(btn3);
	}

}
