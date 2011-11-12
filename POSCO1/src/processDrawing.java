import java.awt.Graphics;

import javax.swing.JComponent;

public class processDrawing extends JComponent {
	private static final long serialVersionUID = 1L;
	Act[] acts = new Act[5];

	processDrawing() {
		for (int i = 0; i < acts.length; i++) {
			
			acts[i] = new Act();
			acts[i].name = "act " + Integer.toString(i);
			acts[i].actor = "act " + Integer.toString(i);
			acts[i].px = i * 200 + 30;
			acts[i].py = 140;

		}
		for (int i = 0; i < acts.length; i++) { // Block 9개 그리기
			Act prev;
			Act next;
			if (i == 0) {
				prev = null;
				next = acts[i + 1];
			} else if (i == acts.length - 1) {
				prev= acts[i - 1];
				next= null;
			} else {
				next= acts[i + 1];
				prev= acts[i - 1];
			}
			acts[i].prevAct = prev;
			acts[i].nextAct = next;
		}
		
	}

	public void paintComponent(Graphics g) {
		for (int i = 0; i < acts.length; i++) {
			acts[i].draw(g);
		}
	}
}
