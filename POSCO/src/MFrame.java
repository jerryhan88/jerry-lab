import java.awt.Dialog;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

public class MFrame extends JFrame implements ActionListener {
	private static final long serialVersionUID = 1L;
	JMenuBar mb = new JMenuBar();

	JMenu mfile = new JMenu("File");
	JMenuItem fexit = new JMenuItem("Exit");

	JMenu viewer = new JMenu("Viewer");
	JMenuItem item_v = new JMenuItem("Items");
	JMenuItem notice_v = new JMenuItem("Notices");
	JMenuItem process_v = new JMenuItem("Process");

	public MFrame() {
		super("POSCO");
		this.init();
	}

	public void init() {
		setJMenuBar(mb);
		mb.add(mfile);
		mb.add(viewer);

		mfile.add(fexit);

		viewer.add(item_v);
		viewer.add(notice_v);
		viewer.add(process_v);

		fexit.addActionListener(this);
		fexit.setActionCommand("exit");

		item_v.addActionListener(this);
		item_v.setActionCommand("item");

		notice_v.addActionListener(this);
		notice_v.setActionCommand("notice");

		process_v.addActionListener(this);
		process_v.setActionCommand("process");
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		String check = e.getActionCommand();
		if (check.equals("exit")) {
			System.exit(0);
		} else if (check.equals("item")) {
//			Dialog info = new Dialog(this, "test", true);
//			info.setSize(140, 190);
//			info.setLocation(50, 50);
//			info.setVisible(true);
//			info.addWindowListener(new WindowAdapter() { // Dialog의 닫기 이벤트
//				public void windowClosing(WindowEvent e) {
//					e.getWindow().setVisible(false);
//					e.getWindow().dispose();
//				}
//			});

			 itemFrame iF = new itemFrame(this);
			 
		} else if (check.equals("notice")) {
			noticeFrame nF = new noticeFrame();
			nF.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
			nF.setBounds(100, 50, 400, 300);
			nF.setResizable(false);
			nF.setVisible(true);
		} else if (check.equals("process")) {
			processFrame pF = new processFrame();
			pF.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
			pF.setBounds(100, 50, 400, 300);
			pF.setResizable(false);
			pF.setVisible(true);
		}
	}
}
