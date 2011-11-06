import java.awt.*;
// 단순히 Ship을 그리는 class 임
public class Ship {

	int x;
	int y;

	void draw(Graphics g) {
		g.drawOval(x, y, 240, 35);
	}
}
