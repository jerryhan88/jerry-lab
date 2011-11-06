import java.awt.*;
import java.util.*;

public class Node implements Comparable<Node> {
	// Node를 그리기 위한 좌표 x,y
	int x;
	int y;
	// 각 Node 들을 쉬게 파악하기
	int id = -1;
	// distance의 초기화를 이렇게 해두어야 정확한 ShortestPathPlan를 할 수 있음
	double distance = Integer.MAX_VALUE;
	// Node에 Tractor가 있는지 없는지 여부를 판단함
	boolean occupied;
	// SPF를 할때 제외해야 할 (다음 Node에 있는 차량이 block인 경우) Node를 표시함
	boolean special;
	// 이전 Node를 기억하기
	Node prev = null;
	// 다음 Node를 기억하기
	Node next = null;
	// 현 Node에 서있는 차량을 기억함
	Tractor nowNodeTracktor = null;
	// 이 Node에서 다른 Node 연결되어 있는 edge들을 가지고 있는 Vector 
	Vector<Edge> edges = new Vector<Edge>();
	// 현 Node의 open과 close를 나타냄  SPF class 에서 SPFcore method에서 이용 됨
	enum NodeState {
		none, open, close
	};
	// Node에 정차할 수 있는 방향을 정해 줌
	enum destinationState {
		none, east, west
	}

	NodeState state = NodeState.none;
	destinationState nodeDirection = destinationState.none;

	Node() {
	}
	// NodeState의 상태를 설정함
	public void setState(NodeState ns) {
		state = ns;
	}
	// destinationState의 상태를 설정함
	public void setDirection(destinationState ds) {
		nodeDirection = ds;
	}
	// 이 Node에 tractor가 들어 왔다고 설정 함
	public void setOccupy(Tractor t) {
		occupied = true;
		nowNodeTracktor = t;
	}
	// Node에서 tractor가 빠져 나갔음을 설정
	public void setNotOcuupy() {
		occupied = false;
		nowNodeTracktor = null;
	}
	
	public void addEdge(Node via) {
		Edge e = new Edge();
		e.setEdge(via);
		// edge의 방향을 정해 주기 위한 code임  Node마다 가지고 있는 id를 이용하여 네가지 방향으로 나눴음
		if (id - e.nextNode.id == -1) {
			e.setState(Edge.EdgeState.East);
		} else if (id - e.nextNode.id == 1) {
			e.setState(Edge.EdgeState.West);
		} else if (id - e.nextNode.id < -1) {
			e.setState(Edge.EdgeState.South);
		} else {
			e.setState(Edge.EdgeState.North);
		}
		// 방향을 설정한뒤 edges에 저장해 둠
		edges.add(e);
	}
	// priorityQueue와 이어지는 code임  이 code로 인하여 distance의 수치가 가장 작은 것이 바로 return될 수 있음
	public int compareTo(Node n) {
		if (distance == n.distance) {
			return 0;
		} else if (distance > n.distance) {
			return 1;
		} else {
			return -1;
		}
	}
	// 밑 그림을 그리는 code
	void draw(Graphics g) {
		g.drawOval(x - 15, y - 15, 10, 10);

		for (int i = 0; i < edges.size(); i++) {
			Edge e = edges.get(i);
			drawEdge(g, e.nextNode);
		}
	}
	// edge를 그리는 code로 크게 Line만 그리는 것과 화살표까지 그리는 두가지 나눠짐
	void drawEdge(Graphics g, Node n1) {
		double ax = n1.x - x;
		double ay = n1.y - y;

		double la = Math.sqrt(ax * ax + ay * ay);

		double ux = ax / la;
		double uy = ay / la;

		int sx = x + (int) (ux * 5) - 10;
		int sy = y + (int) (uy * 5) - 10;
		int ex = n1.x - (int) (ux * 5) - 10;
		int ey = n1.y - (int) (uy * 5) - 10;

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
