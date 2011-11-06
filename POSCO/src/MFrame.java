import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

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
		}else if (check.equals("item")) {
			System.out.println("Hello");
		}else if (check.equals("notice")) {
			
		}else if (check.equals("process")) {
		}
	}
}

