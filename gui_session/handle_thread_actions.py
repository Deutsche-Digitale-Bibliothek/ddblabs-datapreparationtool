from lxml import etree

def save_to_xml(action, root_path):

    thread_actions_file = root_path + "/" + "gui_session/thread_actions.xml"
    thread_actions_input = etree.parse(thread_actions_file)

    # Stoppen des Threads
    if action == "stop_thread":
        findlist = thread_actions_input.findall("//stop_processing")
        findlist[0].text = "True"

    if action == "reset_actions":
        findlist = thread_actions_input.findall("//stop_processing")
        findlist[0].text = "False"

    thread_actions_output = open(thread_actions_file, 'wb')
    thread_actions_input.write(thread_actions_output, encoding='utf-8', xml_declaration=True)
    thread_actions_output.close()

def load_from_xml(action, root_path):
    thread_actions_file = root_path + "/" + "gui_session/thread_actions.xml"
    thread_actions_input = etree.parse(thread_actions_file)

    # Stoppen des Threads
    if action == "stop_thread":
        findlist = thread_actions_input.findall("//stop_processing")
        if findlist[0].text == "True":
            return True
        if findlist[0].text == "False":
            return False
