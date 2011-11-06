import java.awt.Color;
import java.awt.Graphics;


public class Act {
	String name;
	String actor;
	
	int px;
	int py;
	
	Act prevAct;
	Act nextAct;
	
	void draw(Graphics g) {
		g.setColor(Color.LIGHT_GRAY);
		g.fillRect(px, py, 240, 60);
	}
}
