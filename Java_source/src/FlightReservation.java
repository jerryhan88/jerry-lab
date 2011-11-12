import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;
import javax.swing.border.EtchedBorder;
import javax.swing.border.TitledBorder;

public class FlightReservation extends JFrame {

	public FlightReservation() {
		super("Flight Reservation Dialog");

		setSize(400, 300);

		JPanel p1 = new JPanel();
		p1.setLayout(new BoxLayout(p1, BoxLayout.X_AXIS));

		JPanel p1r = new JPanel();
		p1r.setBorder(new EmptyBorder(10, 10, 10, 10));

		// Variant1
		p1r.setLayout(new GridLayout(3, 2, 5, 5));
		p1r.add(new JLabel("Date"));
		p1r.add(new JTextField());

		p1r.add(new JLabel("From:"));
		JComboBox cb1 = new JComboBox();
		cb1.addItem("New York");
		p1r.add(cb1);

		p1r.add(new JLabel("To:"));
		JComboBox cb2 = new JComboBox();
		cb2.addItem("London");
		p1r.add(cb2);

		p1.add(p1r);

		JPanel p3 = new JPanel();
		p3.setLayout(new BoxLayout(p3, BoxLayout.Y_AXIS));
		p3.setBorder(new TitledBorder(new EtchedBorder(), "Options"));

		ButtonGroup group = new ButtonGroup();
		JRadioButton r1 = new JRadioButton("Firset class");
		group.add(r1);
		p3.add(r1);
		JRadioButton r2 = new JRadioButton("Business");
		group.add(r2);
		p3.add(r2);
		JRadioButton r3 = new JRadioButton("Coach");
		group.add(r3);
		p3.add(r3);

		p1.add(p3);

		getContentPane().add(p1, BorderLayout.NORTH);

		JPanel p2 = new JPanel(new BorderLayout());
		p2.setBorder(new TitledBorder(new EtchedBorder(), "Available Flights"));
		JList list = new JList();
		JScrollPane ps = new JScrollPane(list);
		p2.add(ps, BorderLayout.CENTER);
		getContentPane().add(p2, BorderLayout.CENTER);

		JPanel p4 = new JPanel();
		JPanel p4c = new JPanel();
		p4c.setLayout(new GridLayout(1, 3, 5, 5));

		JButton b1 = new JButton("Serarch");
		p4c.add(b1);
		JButton b2 = new JButton("Purchase");
		p4c.add(b2);
		JButton b3 = new JButton("Exit");
		p4c.add(b3);

		p4.add(p4c);
		getContentPane().add(p4, BorderLayout.SOUTH);

		WindowListener wndCloser = new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		};
		
		addWindowListener(wndCloser);

		setVisible(true);
	}

	public static void main(String[] args) {
		new FlightReservation();
	}

}
