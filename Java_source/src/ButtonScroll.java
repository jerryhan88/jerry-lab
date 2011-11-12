import java.awt.BorderLayout;
import java.awt.Point;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JViewport;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class ButtonScroll extends JFrame {
	private static final long serialVersionUID = 1L;
	protected JViewport m_viewport;
	protected JButton m_up;
	protected JButton m_down;
	protected JButton m_left;
	protected JButton m_right;

	protected int m_pgVert;
	protected int m_pgHorz;

	public ButtonScroll() {
		super("Scrolling Programmatically");
		setSize(400, 400);
		getContentPane().setLayout(new BorderLayout());

		ImageIcon shuttle = new ImageIcon("pic//flight.gif");
		m_pgVert = shuttle.getIconHeight() / 5;
		m_pgHorz = shuttle.getIconWidth() / 5;
		JLabel lbl = new JLabel(shuttle);

		m_viewport = new JViewport();
		m_viewport.setView(lbl);
		m_viewport.addChangeListener(new ChangeListener() {
			public void stateChanged(ChangeEvent e) {
				enableButtons(ButtonScroll.this.m_viewport.getViewPosition());
			}
		});
		getContentPane().add(m_viewport, BorderLayout.CENTER);

		JPanel pv = new JPanel(new BorderLayout());
		
		setVisible(true);

	}

	protected void enableButtons(Point pt) {
		if (pt.x == 0) {
			enableComponent(m_left, false);
		} else {
			enableComponent(m_left, true);
		}
		if (pt.x >= getMaxXExtent()) {
			enableComponent(m_right, false);
		} else {
			enableComponent(m_right, true);
		}
		
		if (pt.y == 0) {
			enableComponent(m_up, false);
		} else {
			enableComponent(m_up, true);
		}
		if (pt.y >= getMaxYExtent()) {
			enableComponent(m_down, false);
		} else {
			enableComponent(m_down, true);
		}
		
	}

	private int getMaxXExtent() {
		return m_viewport.getView().getWidth() - m_viewport.getWidth();
	}

	private int getMaxYExtent() {
		return m_viewport.getView().getHeight() - m_viewport.getHeight();
	}

	protected void enableComponent(JComponent c, boolean b) {
		if (c.isEnabled() != b) {
			c.setEnabled(b);
		}
	}

	public static void main(String[] args) {
		new ButtonScroll();
	}
}
