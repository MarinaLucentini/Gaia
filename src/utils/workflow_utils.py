def clear_messages_workflow(responses):
    all_messages = []
    for index, resp in enumerate(responses):
        if index == 0:
            prefix = "HumanMessage : "
        else:
            prefix = "AIMessage : "
        try:
            element = next(iter(resp.values()))["messages"]

            if isinstance(element, list):
                element = element[0].content
            else:
                element = element.content
            all_messages.append(prefix + element)
        except:
            pass

    return all_messages
