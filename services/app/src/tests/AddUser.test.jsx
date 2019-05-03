import React from 'react'
import { shallow } from 'enzyme';
import AddUser from '../components/AddUser';
import renderer from 'react-test-renderer';

test('AddUser renders proprely', () => {
    const wrapper = shallow(<AddUser />);
    const formElement = wrapper.find('form');
    const inputElements = formElement.find('input');
    expect(inputElements.length).toBe(3);
    expect(inputElements.get(0).props.name).toBe('username');
    expect(inputElements.get(1).props.name).toBe('email');
    expect(inputElements.get(2).props.name).toBe('submit');
})

test('Add User snapshots renders properly', () => {
    const tree = renderer.create(<AddUser />).toJSON();
    expect(tree).toMatchSnapshot();
})
