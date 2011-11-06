import java.util.*;
import java.awt.*;

public class Tractor {
	Node start;
	Node end;
	// ShortestPathFinding을 한 결과물을 저장할 Vector임
	Vector<Node> Path = new Vector<Node>();
	
	Color pathColor;
	// Tracktor의 번호를 담아둘 value
	int number;
	// stop된 상태에서 1씩 증가하다 10이 되면 출발시키기 위한 value
	int stopTime = 0;
	// 서로 마주 달려오는 차량중 한 Tractor가 active하게 달리는 것을 방지하기 위한 value
	int tmpCount = 0;
	// Tracktor의 상태들을 나타냄
	enum tractorState {
		move, wait, block, stop
	};
	
	tractorState state = tractorState.move;

	public Tractor(Node start, Node end, Color pathColor, int num) {
		this.start = start;
		this.end = end;
		this.pathColor = pathColor;
		this.number = num;
	}
	// 혹시라도 stop상태에서 바로 block이 되는 tracktor들을 위한 method로 그런 상황이 벌어지더라도 start와 end는 기억해둠
	public void saveStartEnd(Node start, Node end) {
		this.start = start;
		this.end = end;
	}
	
	public void savePath(Node newS, Node newE) {
		// Path 초기화 필수 임
		Path.clear();
		this.start = newS;
		this.end = newE;
		Node v = newE;
		// end부터 시작하여 end와 prev 관계에 있는 Node들을 차례 차례 저장 시킴
		while (true) {
			Path.add(v);
			if(v == start) {
				break;
			}
			v = v.prev;
		}
	}

	void drawPath(Graphics g) {
		// 목적지를 그리는 code
		g.setColor(Color.CYAN);
		g.fillOval(end.x - 15, end.y - 15, 10, 10);
		// Path.size()가 계속 변하기 때문에 움직이는거 처럼 보이게 해 줄 수 있게 도와주는 code
		Node first = Path.lastElement();
		g.setColor(pathColor);
		g.fillOval(first.x - 15, first.y - 15, 10, 10);

		for (int i = Path.size()-1; i > 0; i--) {
			Path.get(i).drawEdge(g, Path.get(i -1));
		}
	}
}
