
public class Edge {
	// 현 Node의 edge에 이어진 다음 Node
	Node nextNode;
	
	enum EdgeState {
		none, East, West, South, North
	};
	
	EdgeState state = EdgeState.none;
	
	public void setState(EdgeState ns) {
		state = ns;
	}

	void setEdge(Node via) {
		this.nextNode = via;
	}
}
