# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s gisweb.trigeau -t test_mappa_simulazione.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src gisweb.trigeau.testing.GISWEB_TRIGEAU_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/gisweb/trigeau/tests/robot/test_mappa_simulazione.robot
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

Scenario: As a site administrator I can add a Mappa simulazione
  Given a logged-in site administrator
    and an add Mappa simulazione form
   When I type 'My Mappa simulazione' into the title field
    and I submit the form
   Then a Mappa simulazione with the title 'My Mappa simulazione' has been created

Scenario: As a site administrator I can view a Mappa simulazione
  Given a logged-in site administrator
    and a Mappa simulazione 'My Mappa simulazione'
   When I go to the Mappa simulazione view
   Then I can see the Mappa simulazione title 'My Mappa simulazione'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Mappa simulazione form
  Go To  ${PLONE_URL}/++add++Mappa simulazione

a Mappa simulazione 'My Mappa simulazione'
  Create content  type=Mappa simulazione  id=my-mappa_simulazione  title=My Mappa simulazione

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Mappa simulazione view
  Go To  ${PLONE_URL}/my-mappa_simulazione
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Mappa simulazione with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Mappa simulazione title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
