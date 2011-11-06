import java.awt.Graphics;

import javax.swing.JComponent;


public class processDrawing extends JComponent{
	private static final long serialVersionUID = 1L;
	Act[] acts = new Act[4];
	
	processDrawing() {
		for (int i = 0; i < acts.length; i++) { // Block 9개 그리기
			acts[i] = new Act();
			acts[i].name = "act "+Integer.toString(i);
			acts[i].actor = "act "+Integer.toString(i);
			     
			acts[i].px = 240/* Block 가로 */+ 80 + 50;
			acts[i].py = 30;
			
			if (i == 0) {
				acts[i].prevAct = null;
				acts[i].nextAct = acts[i+1];
			} else if(i == acts.length-1) {
				acts[i].prevAct = acts[i-1];
				acts[i].nextAct = null;
			} else {
				acts[i].nextAct = acts[i+1];
				acts[i].prevAct = acts[i-1];
			}
			
		}
	}
	
	public void paintComponent(Graphics g) {
		for (int i = 0; i < acts.length; i++) {
			acts[i].draw(g);
		}
	}
}
