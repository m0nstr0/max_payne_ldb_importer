import maya.cmds as cmds


def registerMP2NodeTriggerAETemplate():
    mel = '''
 global proc AEMP2_Node_TriggerTemplate( string $nodeName )
{
    editorTemplate -beginScrollLayout;

    editorTemplate -beginLayout "Max Payne 2 :: Trigger" -collapse 0;

        editorTemplate -beginLayout "Base" -collapse 0;
            editorTemplate -beginNoOptimize;
                editorTemplate -label "Hidden12" -addControl "na_hidden";
                editorTemplate -label "Exclude From Game" -addControl "na_excludeFromGame";
                editorTemplate -label "Exclude From Lighting" -addControl "na_excludeFromLighting";
                editorTemplate -label "Enable Export Regrouping" -addControl "na_enableExportRegrouping";
                editorTemplate -addSeparator;
                editorTemplate -callCustom "AEMP2_Node_TriggerTemplate_create_fsm_edit_button" "AEMP2_Node_TriggerTemplate_update_fsm_edit_button" "dummyAttribute";
            editorTemplate -endNoOptimize;
        editorTemplate -endLayout;

        editorTemplate -addSeparator;

        editorTemplate -beginLayout "Trigger" -collapse 0;
            editorTemplate -beginNoOptimize;
                editorTemplate -label "Radius" -addControl "na_radius";
                editorTemplate -addSeparator;
                editorTemplate -label "Player" -addControl "na_player";
                editorTemplate -label "Use" -addControl "na_use";
                editorTemplate -label "Enemy" -addControl "na_enemy";
                editorTemplate -label "Bullet" -addControl "na_bullet";
                editorTemplate -label "Look At" -addControl "na_lookAt";
                editorTemplate -label "Visibility" -addControl "na_visibility";
            editorTemplate -endNoOptimize;
        editorTemplate -endLayout;

        editorTemplate -addSeparator;

        editorTemplate -beginLayout "Activator's Use Animation" -collapse 0;
            editorTemplate -beginNoOptimize;
                editorTemplate -label "Common Animation" -addControl "na_activatorsAnimationCommon";
                editorTemplate -addSeparator;
                editorTemplate -label "Use Custom" -addControl "na_activatorsAnimationUseCustom";
                editorTemplate -label "Custom Animation" -addControl "na_activatorsAnimationCustom"; 
            editorTemplate -endNoOptimize;
        editorTemplate -endLayout;

    editorTemplate -endLayout;

    editorTemplate -addSeparator;

    editorTemplate -addExtraControls;

    editorTemplate -endScrollLayout;
}

//FSM Edit button
global proc AEMP2_Node_TriggerTemplate_create_fsm_edit_button(string $nodeName)
{
    button -label "Edit FSM" -command "AEMP2_Node_TriggerTemplate_update_fsm_button_command" mp2FsmEditorButton;
}

global proc AEMP2_Node_TriggerTemplate_update_fsm_edit_button(string $nodeName)
{
    button -e -command "AEMP2_Node_TriggerTemplate_update_fsm_button_command" mp2FsmEditorButton;
}

global proc AEMP2_Node_TriggerTemplate_update_fsm_button_command() {
    print("Button clicked! Running custom logic...");
}
//FSM Edit button



global proc myLocatorAE_create_mel(string $nodeName)
{
    python("from max_payne_maya.mp2nodes.mp2_node_level_item_ui import myLocatorAE_create; myLocatorAE_create('" + $nodeName + "')");
}

global proc myLocatorAE_update_mel(string $nodeName)
{
    python("from max_payne_maya.mp2nodes.mp2_node_level_item_ui import myLocatorAE_update; myLocatorAE_update('" + $nodeName + "')");
}

global proc AEAddFSMEditorButtonNew(string $attrName)
{
    columnLayout -adjustableColumn true;
    button -label "Execute Action" -command "myCustomCommand" myCustomButton;

    optionMenuGrp -l "Position";
    menuItem -label "Left";
    menuItem -label "Center";
    menuItem -label "Right";
}

// 3. Procedure to UPDATE the button (called when node is re-selected)
global proc AEmyButtonReplace(string $attrName) {
    // Update the button command if it depends on the specific node name
    button -e -command "myCustomCommand" myCustomButton;
}

// 4. The command the button will run

    '''
    cmds.eval(mel)
