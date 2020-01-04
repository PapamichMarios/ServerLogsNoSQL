import React from 'react';

import { NavLink, withRouter } from "react-router-dom";
import { Navbar, Nav, NavItem, Button } from 'react-bootstrap';
import { FaHome, FaPlus } from 'react-icons/fa';

class NavBar extends React.Component {

    render() {

        // for the left part of the navbar
        let navLeft = (
            <Nav className="mr-auto">
                <NavItem className="button-margin-left">
                    <NavLink to="/api-methods">
                        <Button title="API Methods" variant="dark" style={{borderRadius: '12px'}}>
                            <b>API Methods</b>
                        </Button>
                    </NavLink>
                </NavItem>

                <NavItem className="button-margin-left">
                    <NavLink to="/cast-upvote">
                        <Button title="Cast Upvote" variant="dark" style={{borderRadius: '12px'}}>
                            <b>Cast Upvote</b>
                        </Button>
                    </NavLink>
                </NavItem>
            </Nav>
        );

        // for the right part of the navbar
        let navRight = (
            <Nav className="justify-content-end">
                <NavItem className="button-margin">
                    <NavLink to="/insert-log">
                        <Button title="Insert Log" variant="dark" style={{borderRadius: '12px'}}>
                            <FaPlus style={{verticalAlign: 'baseline'}} />
                        </Button>
                    </NavLink>
                </NavItem>

                <NavItem className="button-margin">
                    <NavLink to="/home">
                        <Button title="Home" variant="dark" style={{borderRadius: '12px'}}>
                        <FaHome style={{verticalAlign: 'baseline'}} />
                        </Button>
                    </NavLink>
                </NavItem>
            </Nav>
        );

        return (
             <Navbar bg="dark" variant="dark" style={{marginBottom: '15px'}}>
                  <Navbar.Brand href="/welcome"> <b> LogDB </b> </Navbar.Brand>
                  <Navbar.Toggle aria-controls="basic-navbar-nav" />
                  <Navbar.Collapse id="basic-navbar-nav">

                  {navLeft}

                  {navRight}

                  </Navbar.Collapse>
              </Navbar>
        );
    }
}

export default withRouter(NavBar);