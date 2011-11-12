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

public class SplitSample extends JFrame {
	private static final long serialVersionUID = 1L;
	protected JSplitPane m_sp;

	public SplitSample() {
		super("Simple SplitSample Example");
		setSize(400, 400);

		Component c11 = new SimplePanel();
		Component c12 = new SimplePanel();
		JSplitPane spLeft = new JSplitPane(JSplitPane.VERTICAL_SPLIT, c11, c12);
		spLeft.setDividerSize(4);
		spLeft.setContinuousLayout(true);

		Component c21 = new SimplePanel();
		Component c22 = new SimplePanel();

		JSplitPane spRight = new JSplitPane(JSplitPane.VERTICAL_SPLIT, c21, c22);
		spRight.setDividerSize(8);
		spRight.setContinuousLayout(true);

		m_sp = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, spLeft, spRight);
		m_sp.setContinuousLayout(false);
		//m_sp.setOneTouchExpandable(true);
		
		getContentPane().add(m_sp, BorderLayout.CENTER);
		
		WindowListener wndCloser = new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		};
		
		addWindowListener(wndCloser);

		setVisible(true);
	}
	
	public static void main(String[] args) {
		new SplitSample();
	}

}

class SimplePanel extends JPanel {
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
