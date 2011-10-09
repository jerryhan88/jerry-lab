package startingJFrame;

import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.GridLayout;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.TitledBorder;

public class BorderFlowJPanel extends JPanel {
	private static final long serialVersionUID = 1L;
	JPanel eastp = new JPanel();
	JPanel westp = new JPanel();
	JPanel northp = new JPanel();
	JPanel southp = new JPanel();
	JPanel centerp = new JPanel();

	JLabel titlelb = new JLabel("", JLabel.CENTER);

	JButton jButton1 = new JButton("안    경");
	JButton jButton2 = new JButton();
	JButton jButton3 = new JButton("인사과");
	JButton jButton4 = new JButton("총부과");
	JButton jButton5 = new JButton("서무과");
	JButton jButton6 = new JButton("경리과");
	JButton jButton7 = new JButton("핸드폰");
	JButton jButton8 = new JButton("컴퓨터");

	public BorderFlowJPanel() {
		System.out.println(this.getClass().getName() + "    start!!");
		inits();
	}

	void inits() {
		this.setLayout(new BorderLayout());
		titlelb.setFont(new java.awt.Font("Arial", Font.BOLD, 20));
		titlelb.setBorder(new TitledBorder("Title Label"));
		titlelb.setText("BorderLayout And FlowLayout");
		
		northp.setLayout(new BorderLayout());
		northp.add(titlelb, BorderLayout.SOUTH);
		this.add(northp, BorderLayout.NORTH);
		
		centerp.setBorder(new TitledBorder("Center"));
		centerp.add(jButton3);
		centerp.add(jButton4);
		centerp.add(jButton5);
		centerp.add(jButton6);
		this.add(centerp, BorderLayout.CENTER);
		
		jButton2.setText("Add");
		westp.setBorder(new TitledBorder("West"));
		westp.add(jButton2);
		this.add(westp, BorderLayout.WEST);
		
		southp.setBorder(new TitledBorder("South"));
		this.add(southp, BorderLayout.SOUTH);
		
		eastp.setBorder(new TitledBorder("East"));
		eastp.setLayout(new GridLayout(3,1));
		eastp.add(jButton8);
		eastp.add(jButton7);
		eastp.add(jButton1);
		this.add(eastp, BorderLayout.EAST);
	}
}
