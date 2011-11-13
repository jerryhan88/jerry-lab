import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.swing.JFrame;
import javax.swing.JLabel;

public class MFrame extends JFrame {
	private static final long serialVersionUID = 1L;

	// public JPanel itemP = new JPanel(new BorderLayout());
	int iPpx = 10;
	int iPpy = 30;
	int iPsx = 600;
	int iPsy = 350;

	int nPpx = iPpx + iPsx + 10;
	int nPpy = iPpy;
	int nPsx = 1024 - (nPpx + 15);
	int nPsy = iPsy;

	int pPpx = iPpx;
	int pPpy = iPpy + iPsy + 30;
	int pPsx = 1024 - 25;
	int pPsy = 768 - (pPpy + 50);

	itemPanel itemP;
	noticePanel noticeP;
	processPanel processP;

	public MFrame() {
		super("POSCO");
		this.setLayout(null);
		setBounds(100, 50, 1024, 768);
		JLabel items = new JLabel("Items");
		items.setBounds(iPpx + 5, iPpy - 25, 50, 20);
		this.add(items);
		JLabel notices = new JLabel("Notices");
		notices.setBounds(nPpx + 5, nPpy - 25, 50, 20);
		this.add(notices);

		JLabel processes = new JLabel("Process");
		processes.setBounds(pPpx + 5, pPpy - 25, 50, 20);
		this.add(processes);

		itemP = new itemPanel(iPpx, iPpy, iPsx, iPsy);
		noticeP = new noticePanel(nPpx, nPpy, nPsx, nPsy, "127.0.0.1", 5420);
		noticeP.giveAndTake();
		processP = new processPanel(pPpx, pPpy, pPsx, pPsy);

		this.add(itemP);
		// itemP.setBackground(new java.awt.Color(150));
		// itemP.setBounds(iPpx, iPpy, iPsx, iPsy);
		this.add(noticeP);
		this.add(processP);
//		processP.setBackground(new java.awt.Color(150));
		WindowListener wndCloser = new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		};
		addWindowListener(wndCloser);
		setVisible(true);
		
		
	}
}
