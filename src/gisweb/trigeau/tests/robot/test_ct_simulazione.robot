# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s gisweb.trigeau -t test_simulazione.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src gisweb.trigeau.testing.GISWEB_TRIGEAU_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/gisweb/trigeau/tests/robot/test_simulazione.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Simulazione
  Given a logged-in site administrator
    and an add Simulazione form
   When I type 'My Simulazione' into the title field
    and I submit the form
   Then a Simulazione with the title 'My Simulazione' has been created

Scenario: As a site administrator I can view a Simulazione
  Given a logged-in site administrator
    and a Simulazione 'My Simulazione'
   When I go to the Simulazione view
   Then I can see the Simulazione title 'My Simulazione'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Simulazione form
  Go To  ${PLONE_URL}/++add++Simulazione

a Simulazione 'My Simulazione'
  Create content  type=Simulazione  id=my-simulazione  title=My Simulazione

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Simulazione view
  Go To  ${PLONE_URL}/my-simulazione
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Simulazione with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Simulazione title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
