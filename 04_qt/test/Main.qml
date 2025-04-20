import QtQuick

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Simple_Layout")

    Rectangle {
        id: header
        width: parent.width
        height: 100
        color: "gray"
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        Text {
            text: "header"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    Rectangle {
        color: "coral"
        anchors.top: header.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: footer.top

        Text {
            text: "info"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    Rectangle {
        id: footer
        width: parent.width
        height: 100
        color: "gray"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        Rectangle {
            width: parent.width / 3 - 10
            height: parent.height / 2
            color: "sky blue"
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            Text {
                text: "<--"
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        Rectangle {
            width: parent.width / 3 - 10
            height: parent.height / 2
            color: "sky blue"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter

            Text {
                text: "<-->"
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        Rectangle {
            width: parent.width / 3 - 10
            height: parent.height / 2
            color: "sky blue"
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter

            Text {
                text: "-->"
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
    }
}
