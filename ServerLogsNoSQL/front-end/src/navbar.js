import React from 'react';

import { NavLink, withRouter } from "react-router-dom";
import { Navbar, Nav, NavItem, Button } from 'react-bootstrap';
import { FaHome } from 'react-icons/fa';

class NavBar extends React.Component {

    render() {

        // for the left part of the navbar
        let navLeft = (
            <Nav className="mr-auto">
                {/* <NavItem className="button-margin-left">
                <Link to="/procedure1">
                    <Button title="Procedure 1" variant="dark" style={{borderRadius: '12px'}}>
                        <b>Procedure 1</b>
                    </Button>
                </Link>
                </NavItem>

                <NavItem className="button-margin-left">
                <Link to="/procedure2">
                    <Button title="Procedure 2" variant="dark" style={{borderRadius: '12px'}}>
                        <b>Procedure 2</b>
                    </Button>
                </Link>
                </NavItem>

                <NavItem className="button-margin-left">
                <Link to="/procedure3">
                    <Button title="Procedure 3" variant="dark" style={{borderRadius: '12px'}}>
                        <b>Procedure 3</b>
                    </Button>
                </Link>
                </NavItem>

                <NavItem className="button-margin-left">
                <Link to="/search-ip">
                    <Button title="Search IP" variant="dark" style={{borderRadius: '12px'}}>
                        <b>Search IP</b>
                    </Button>
                </Link>
                </NavItem> */}
            </Nav>
        );

        // for the right part of the navbar
        let navRight = (
            <Nav className="justify-content-end">
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