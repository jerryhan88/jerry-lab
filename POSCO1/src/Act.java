import java.awt.Color;
import java.awt.Graphics;

public class Act {
	String name;
	String actor;

	int px;
	int py;

	Act prevAct;
	Act nextAct;

	boolean noneNext = false;

	void draw(Graphics g) {
		g.setColor(Color.LIGHT_GRAY);
		g.fillRect(px, py, 150, 100);
		g.setColor(Color.BLACK);
//		g.drawString(name, px + 65, py+ 120);
		if (nextAct != null) {
			drawEdge(g, nextAct);
		}
	}

	void drawEdge(Graphics g, Act nextA) {
		double ax = nextA.px - px;
		double ay = nextA.py - py;

		double la = Math.sqrt(ax * ax + ay * ay);

		double ux = ax / la;
		double uy = ay / la;

		int sx = px + 150;
		int sy = py + 50;
		int ex = nextA.px - 1;
		int ey = nextA.py + 50;

		double px = -uy;
		double py = ux;
		// Node와 Node 사이를 선으로 이어줌
		g.drawLine(sx, sy, ex, ey);
		// 이어진 Node에 화살표까지
		g.drawLine(ex, ey, ex - (int) (ux * 5) + (int) (px * 3), ey
				- (int) (uy * 5) + (int) (py * 3));
		g.drawLine(ex, ey, ex - (int) (ux * 5) - (int) (px * 3), ey
				- (int) (uy * 5) - (int) (py * 3));
	}
}
