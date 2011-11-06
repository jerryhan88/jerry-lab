import java.util.*;

public class SPF {
	// Graph class의 Node들을 저장할 Vector
	Vector<Node> Nodes = new Vector<Node>();
	// 여기서 PriorityQueue는 자신이 가진 Node들의 distance 중 가장 작은 값이 return 되도록 되어 있음
	PriorityQueue<Node> openNodes = new PriorityQueue<Node>();
	// ShorthestPathFinding의 성공 여부를 따지기 위한 변수임
	boolean success = true;

	SPF() {
	}

	// Graph class에서 정의된 Node들을 저장하는 method
	public void addNode(Node n) {
		Nodes.add(n);
	}

	// ShortestPathFinding 이라는 method를 쓸때 재일 먼저 Node들의 상태를 초기화 시킴
	public void reset() {
		for (int i = 0; i < Nodes.size(); i++) {
			Node clearNode = Nodes.get(i);
			clearNode.state = Node.NodeState.none;
			clearNode.distance = Integer.MAX_VALUE;
			clearNode.prev = null;
			clearNode.next = null;
		}
		openNodes.clear();
		success = true;
	}

	// Dijkstra 알고리즘을 푸는 Method
	public void ShortestPathFinding(Node start, Node end) {
		// 처음과 끝의 Node를 입력받은 뒤 Node 전체를 reset 시키고 시작함
		reset();
		Node startNode = null;
		Node endNode = null;
		// 출발지나 목적지에 Yard Tractor 들이 서있는 방향을 고려한 작업 임
		switch (start.nodeDirection) {
		// Yard Tractor가 바라보는 방향으로 출발을 해야함
		case east:
			// 따라서 nodeDirection이 east인 경우 오른쪽으로 한칸을 가게 함
			startNode = Nodes.get(start.id + 1);
			start.special = true;
			break;
		case west:
			// 그리고 nodeDirection이 west인 경우 왼쪽으로 한칸을 가게 함
			startNode = Nodes.get(start.id - 1);
			start.special = true;
			break;
		default:
			// 또 방향이 없는 경우
			// 이 경우는 출발지나 목적지가 아닌 Node에서 새로운 PathPlan을 하는 경우에 실행됨
			startNode = start;
			break;
		}
		// 위에 있는 start의 nodeDirection을 보는 것과 같은 이치임
		// start의 nodeDirection을 볼때와 차이가 있다면 end의 special이라는 value를 조작 함으로써 end가
		// PathPlan을 할때 영향을 주는 것을 방지함
		// special 변수의 보충설명은 아래에 있는 SPFcore 라는 method에서 볼 수 있음
		switch (end.nodeDirection) {
		case east:
			// east인 경우 그 바로 왼쪽이 endNode가 된다
			endNode = Nodes.get(end.id - 1);
			end.special = true;
			break;
		case west:
			endNode = Nodes.get(end.id + 1);
			end.special = true;
			break;
		default:
			break;
		}
		// 여기서 중요한것은 입력 받은 start와 end가 아니 그 앞의(start의 앞=startNode), 그 뒤의(end의
		// 뒤=endNode) Node까지 Dijkstra 알고리즘을 품
		SPFcore(startNode, endNode);

		if (success) {
			// SPFcore가 성공적으로 수행된 경우(startNode가 endNode까지 distance를 update 했을
			// 경우)에 실행됨
			// 일단 start와 end의 special을 초기화 시킨다
			if (start.special || end.special) {
				start.special = false;
				end.special = false;
			}
			// 처음의 의도대로 start와 end까지의 최단거리를 구할려면 startNode와 endNode를 start나 end에
			// prev와 next를 이용하여 이어 주어야
			if (start != startNode) {
				// Tractor가 출발지나 목적지가 아닌 경우 이 작업은 필요 없음
				startNode.prev = start;
				start.next = startNode;
			}
			end.prev = endNode;
			endNode.next = end;

			Node tmp = end;
			// SPFcore로 서로 prev로 연결 되어 있는 Node들을 next로 한번 더 연결 시킴
			while (true) {
				tmp.prev.next = tmp;
				tmp = tmp.prev;
				if (tmp == start)
					break;
			}
			// Console에 SPFcore의 결과물을 출려 시킴
			System.out.print(start.id + " -> ");
			tmp = start;
			while (tmp.next != null) {
				tmp = tmp.next;
				System.out.print(tmp.id);
				if (tmp.next != null) {
					System.out.print(" -> ");
				}
			}
			System.out.println();
		}
	}

	// priorityQueue에 저장되어 있는 Node들 중에 distance가 가장 작은 Node 가 return 되게 함
	public Node getMinVertex() {
		Node v_min = (Node) openNodes.poll();

		return v_min;
	}

	// 각각의 Node들의 distance를 update시키는 method
	private void updateDistance(Node start, Node nextNode, Edge e) {
		double tmpDist;
		// 일반적인 Dijkstra와 다르게 여기선 turn을 할때 가중치를 더 줌으로써 가능한 Tractor가 turn을 하지 않도록 함
		if (start.prev == null) {
			// start는 prev가 없기에 필요한 code임
			tmpDist = start.distance + 1;
		} else {
			// 현재 Node edge의 방향과 이전의 Node의 edge 방향을 비교했을때 방향이 같이 않으면 가중치를 더 줘야함
			Edge prevEdge = null;
			
			for (int j = 0; j < start.prev.edges.size(); j++) {
				if (start.prev.edges.get(j).nextNode == start) {
					prevEdge = start.prev.edges.get(j);
				}
			}
			if (prevEdge.state == e.state) {
				tmpDist = start.distance + 1;
			} else {
				tmpDist = start.distance + 1.1;
			}
		}
		// nextNode의 distance와 prev를 update 시킨다
		if (tmpDist < nextNode.distance) {
			nextNode.distance = tmpDist;
			nextNode.prev = start;
		}
	}

	// Dijkstra 알고리즘의 핵심이 되는 부분
	private Node SPFcore(Node startNode, Node endNode) {
		Node start = startNode;
		start.distance = 0;
		do {
			// Dijkstra의 기본에 따라 Node를 close 시킴
			start.setState(Node.NodeState.close);
			for (int i = 0; i < start.edges.size(); i++) {
				Node nextNode = start.edges.get(i).nextNode;
				// 한번 open 시킨 Node를 한번더 close 혹은 open 시키는 것을 방지
				// nextNode에 다른 Yard Tractor가 있는 경우 그 Node는 제외
				if (nextNode.special || nextNode.state != Node.NodeState.none)
					continue;
				nextNode.setState(Node.NodeState.open);
				// open된 Node들을 priorityQueue에 담아 둠
				openNodes.add(nextNode);

				Edge e = start.edges.get(i);
				// 현재 Node에서 다음 Node의 distance를 update 하도록 함
				// 주의! 이 code는 openNodes 안에 있는 Node만 update 시키도록 되어 있음
				updateDistance(start, nextNode, e);
			}
			// openNodes안에 있는 Node중 distance가 가장 작은 Node를 start로 만듬
			start = getMinVertex();
			if (start == endNode) {
				// while 구문을 계속 실행 시키다 start가 endNode와 같아 지면 while 구문을 끝냄
				break;
			} else if (start == null) {
				// SPFcore가 원하는 start를 end까지 update를 못 시키는 경우
				if (Math.abs(startNode.id - endNode.id) != 1) {
					// 그 중에서도 바로 옆의 Node로 가는 것이 아니라면 success를 false 시켜 Tractor를
					// block 시킨다
					success = false;
				}
				break;
			}
		} while (true);
		return start;
	}
}