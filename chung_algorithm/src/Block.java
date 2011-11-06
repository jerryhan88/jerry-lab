import java.awt.*;
// 단순히 Block을 그리는 Class 
public class Block {
	int x;
	int y;

	void draw(Graphics g) {
		g.setColor(Color.LIGHT_GRAY);
		g.fillRect(x, y, 240, 60);
	}

}
