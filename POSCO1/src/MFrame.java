import java.awt.BorderLayout;

import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JSplitPane;

public class MFrame extends JFrame {
	private static final long serialVersionUID = 1L;
	// public JPanel itemP = new JPanel(new BorderLayout());
	Component itemP;
	Component noticeP;
	Component processP;

	protected JSplitPane m_sp;

	public MFrame() {
		super("POSCO");
		setBounds(100, 50, 1024, 768);

		itemP = new itemPanel();
		noticeP = new noticePanel("127.0.0.1", 5420);
		processP = new processPanel();
		
		JSplitPane spUp = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, itemP,
				noticeP);
		spUp.setDividerLocation(600);
		spUp.setDividerSize(4);
		spUp.setContinuousLayout(true);

		
		m_sp = new JSplitPane(JSplitPane.VERTICAL_SPLIT, spUp, processP);
		m_sp.setDividerLocation(350);
		m_sp.setDividerSize(4);
		m_sp.setContinuousLayout(false);
		getContentPane().add(m_sp, BorderLayout.CENTER);

		/*
		 * JLabel items = new JLabel("Items"); items.setBounds(iPpx + 5, iPpy -
		 * 25, 50, 20); this.add(items); JLabel notices = new JLabel("Notices");
		 * notices.setBounds(nPpx + 5, nPpy - 25, 50, 20); this.add(notices);
		 * 
		 * JLabel processes = new JLabel("Process"); processes.setBounds(pPpx +
		 * 5, pPpy - 25, 50, 20); this.add(processes);
		 * 
		 * itemP = new itemPanel(iPpx, iPpy, iPsx, iPsy); noticeP = new
		 * noticePanel(nPpx, nPpy, nPsx, nPsy, "127.0.0.1", 5420);
		 * noticeP.giveAndTake(); processP = new processPanel(pPpx, pPpy, pPsx,
		 * pPsy);
		 * 
		 * this.add(itemP); // itemP.setBackground(new java.awt.Color(150)); //
		 * itemP.setBounds(iPpx, iPpy, iPsx, iPsy); this.add(noticeP);
		 * this.add(processP); // processP.setBackground(new
		 * java.awt.Color(150));
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
		new MFrame();
	}
}

class SimPanel extends JPanel {
	private static final long serialVersionUID = 1L;

	public Dimension getPreferredSize() {
		return new Dimension(200, 200);
	}

	public Dimension getMinimumSize() {
		return new Dimension(40, 40);
	}

	public void paintComponent(Graphics g) {
		g.setColor(Color.black);
		Dimension sz = getSize();
		g.drawLine(0, 0, sz.width, sz.height);
		g.drawLine(sz.width, 0, 0, sz.height);
	}
}