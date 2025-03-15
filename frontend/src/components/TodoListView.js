import TodoItem from "./Todo";


function TodoView(props) {
    return (
        <div>
            <ul>
                {props.todoList.map(todo => 
                <TodoItem
                todo={todo}
                onDelete={props.onDelete}
                />)}
            </ul>
        </div>
    )
}

export default TodoView