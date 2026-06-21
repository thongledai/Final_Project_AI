def child_node(node,action):
    next_state=result(

                    node.state,

                    action

                    )

    return Node(

                state=next_state,

                parent=node,

                action=action,

                cost=node.cost+1

                )